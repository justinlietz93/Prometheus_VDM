#include "ViewportWindow.h"

#include <QFileInfo>
#include <QVTKOpenGLNativeWidget.h>

#include <vtkGenericOpenGLRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkCamera.h>
#include <vtkNamedColors.h>

#include <vtkAxesActor.h>
#include <vtkOrientationMarkerWidget.h>

#include <vtkCubeSource.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>

#include <vtkXMLImageDataReader.h>
#include <vtkXMLPolyDataReader.h>
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkDataSetSurfaceFilter.h>
#include <vtkSmartVolumeMapper.h>
#include <vtkVolume.h>
#include <vtkVolumeProperty.h>
#include <vtkColorTransferFunction.h>
#include <vtkPiecewiseFunction.h>
#include <vtkPointData.h>

ViewportWindow::ViewportWindow(QWidget* parent)
    : QMainWindow(parent) {
  setupUi();
  setupScene();
}

ViewportWindow::~ViewportWindow() = default;

void ViewportWindow::setupUi() {
  // Create and attach the VTK widget and render window
  m_vtkWidget = new QVTKOpenGLNativeWidget(this);
  setCentralWidget(m_vtkWidget);
  m_vtkWidget->setRenderWindow(m_renderWindow.GetPointer());

  setWindowTitle(QStringLiteral("VDM Nexus — Viewport (Qt + VTK)"));
}

void ViewportWindow::setupScene() {
  // Renderer and background
  vtkNew<vtkNamedColors> colors;
  m_renderer->SetBackground(colors->GetColor3d("SlateGray").GetData());
  m_renderWindow->AddRenderer(m_renderer.GetPointer());

  // Orientation marker (axes in a corner)
  vtkNew<vtkAxesActor> axes;
  m_orientation = vtkSmartPointer<vtkOrientationMarkerWidget>::New();
  m_orientation->SetOrientationMarker(axes.GetPointer());

  // Prefer the widget's interactor if available, else fallback to render window interactor
  auto iren = m_vtkWidget->interactor();
  if (!iren) {
    iren = m_renderWindow->GetInteractor();
  }
  if (iren) {
    m_orientation->SetInteractor(iren);
    m_orientation->SetViewport(0.0, 0.0, 0.20, 0.20);
    m_orientation->SetEnabled(1);
    m_orientation->InteractiveOff();
  }

  // Default demo geometry: cube
  vtkNew<vtkCubeSource> cube;
  cube->SetXLength(0.5);
  cube->SetYLength(0.5);
  cube->SetZLength(0.5);

  vtkNew<vtkPolyDataMapper> mapper;
  mapper->SetInputConnection(cube->GetOutputPort());

  m_actor = vtkSmartPointer<vtkActor>::New();
  m_actor->SetMapper(mapper.GetPointer());
  m_actor->GetProperty()->SetColor(colors->GetColor3d("LightSteelBlue").GetData());

  m_renderer->AddActor(m_actor);
  m_renderer->ResetCamera();
  m_renderWindow->Render();
}

void ViewportWindow::clearScene() {
  if (m_actor) {
    m_renderer->RemoveActor(m_actor);
    m_actor = nullptr;
  }
  if (m_volume) {
    m_renderer->RemoveVolume(m_volume);
    m_volume = nullptr;
  }
  // Keep orientation marker; remove other props if any
  // m_renderer->RemoveAllViewProps(); // avoid removing orientation overlays
}

void ViewportWindow::openPath(const QString& path) {
  QFileInfo fi(path);
  if (!fi.exists()) {
    return;
  }
  const auto ext = fi.suffix().toLower();

  // Reset previous scene content (but keep axes overlay)
  clearScene();

  if (ext == "vti") {
    // Volume rendering for ImageData
    vtkNew<vtkXMLImageDataReader> rdr;
    rdr->SetFileName(path.toUtf8().constData());
    rdr->Update();

    double range[2] = {0.0, 1.0};
    if (auto scal = rdr->GetOutput()->GetPointData()->GetScalars()) {
      scal->GetRange(range);
    }

    vtkNew<vtkColorTransferFunction> ctf;
    ctf->AddRGBPoint(range[0], 0.0, 0.0, 0.0);
    ctf->AddRGBPoint(0.5 * (range[0] + range[1]), 0.6, 0.7, 0.9);
    ctf->AddRGBPoint(range[1], 1.0, 1.0, 1.0);

    vtkNew<vtkPiecewiseFunction> otf;
    // Conservative default opacity ramp
    otf->AddPoint(range[0], 0.00);
    otf->AddPoint(0.5 * (range[0] + range[1]), 0.05);
    otf->AddPoint(range[1], 0.2);

    vtkNew<vtkSmartVolumeMapper> vmap;
    vmap->SetBlendModeToComposite();
    vmap->SetInputConnection(rdr->GetOutputPort());

    vtkNew<vtkVolumeProperty> vprop;
    vprop->SetColor(ctf.GetPointer());
    vprop->SetScalarOpacity(otf.GetPointer());
    vprop->SetInterpolationTypeToLinear();
    vprop->ShadeOn();
    vprop->SetAmbient(0.2);
    vprop->SetDiffuse(0.7);
    vprop->SetSpecular(0.1);

    m_volume = vtkSmartPointer<vtkVolume>::New();
    m_volume->SetMapper(vmap.GetPointer());
    m_volume->SetProperty(vprop.GetPointer());

    m_renderer->AddVolume(m_volume);
    m_renderer->ResetCamera();
    m_renderWindow->Render();
    return;
  }

  if (ext == "vtp") {
    vtkNew<vtkXMLPolyDataReader> rdr;
    rdr->SetFileName(path.toUtf8().constData());
    rdr->Update();

    vtkNew<vtkPolyDataMapper> mapper;
    mapper->SetInputConnection(rdr->GetOutputPort());
    mapper->ScalarVisibilityOff();

    vtkNew<vtkNamedColors> colors;
    m_actor = vtkSmartPointer<vtkActor>::New();
    m_actor->SetMapper(mapper.GetPointer());
    m_actor->GetProperty()->SetColor(colors->GetColor3d("AliceBlue").GetData());

    m_renderer->AddActor(m_actor);
    m_renderer->ResetCamera();
    m_renderWindow->Render();
    return;
  }

  if (ext == "vtu") {
    vtkNew<vtkXMLUnstructuredGridReader> rdr;
    rdr->SetFileName(path.toUtf8().constData());
    rdr->Update();

    vtkNew<vtkDataSetSurfaceFilter> surf;
    surf->SetInputConnection(rdr->GetOutputPort());

    vtkNew<vtkPolyDataMapper> mapper;
    mapper->SetInputConnection(surf->GetOutputPort());
    mapper->ScalarVisibilityOff();

    vtkNew<vtkNamedColors> colors;
    m_actor = vtkSmartPointer<vtkActor>::New();
    m_actor->SetMapper(mapper.GetPointer());
    m_actor->GetProperty()->SetColor(colors->GetColor3d("LightGoldenrodYellow").GetData());

    m_renderer->AddActor(m_actor);
    m_renderer->ResetCamera();
    m_renderWindow->Render();
    return;
  }

  if (ext == "json") {
    // Placeholder: run-manifest viewer/validator will be wired later.
    // For now, ignore silently to keep GUI read-only and stable.
    m_renderWindow->Render();
    return;
  }

  // Unknown extension: keep default cube
  m_renderWindow->Render();
}