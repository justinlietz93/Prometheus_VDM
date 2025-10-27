#include <QApplication>
#include <QSurfaceFormat>
#include <QVTKOpenGLNativeWidget.h>
#include <QString>
#include "ViewportWindow.h"

int main(int argc, char* argv[]) {
  QApplication app(argc, argv);

  // Configure an OpenGL context suitable for VTK on Qt6
  QSurfaceFormat fmt = QSurfaceFormat::defaultFormat();
  fmt.setRenderableType(QSurfaceFormat::OpenGL);
  fmt.setProfile(QSurfaceFormat::CoreProfile);
  fmt.setVersion(3, 2);
  QSurfaceFormat::setDefaultFormat(fmt);
  QVTKOpenGLNativeWidget::setDefaultFormat(fmt);

  ViewportWindow win;
  win.resize(1280, 800);
  win.show();

  if (argc > 1) {
    win.openPath(QString::fromUtf8(argv[1]));
  }

  return app.exec();
}