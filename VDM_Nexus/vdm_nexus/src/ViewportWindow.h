#pragma once

#include <QMainWindow>
#include <QString>

#include <vtkNew.h>
#include <vtkSmartPointer.h>

// Forward declares to keep compile units minimal
class QVTKOpenGLNativeWidget;

class vtkGenericOpenGLRenderWindow;
class vtkRenderer;
class vtkActor;
class vtkVolume;
class vtkOrientationMarkerWidget;

class ViewportWindow : public QMainWindow {
  Q_OBJECT
public:
  explicit ViewportWindow(QWidget* parent = nullptr);
  ~ViewportWindow() override;

  // Opens a path for preview:
  // - .vti (ImageData): simple volume render
  // - .vtp (PolyData), .vtu (UnstructuredGrid): surface render
  // - .json: (run-manifest) stub handled later; for now no-op
  void openPath(const QString& path);

private:
  void setupUi();
  void setupScene();
  void clearScene();

private:
  QVTKOpenGLNativeWidget* m_vtkWidget = nullptr;
  vtkNew<vtkGenericOpenGLRenderWindow> m_renderWindow;
  vtkNew<vtkRenderer> m_renderer;

  vtkSmartPointer<vtkActor> m_actor;   // surface actor (vtp/vtu/demo cube)
  vtkSmartPointer<vtkVolume> m_volume; // volume actor (vti)
  vtkSmartPointer<vtkOrientationMarkerWidget> m_orientation;
};