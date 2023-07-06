from os import path
from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import cmake_layout, CMake, CMakeToolchain


class MathglTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "VirtualRunEnv"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)
        self.requires("qt/5.15.9")
        self.requires("opengl/system")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["WITH_QT"] = self.dependencies["mathgl"].options.qt5
        tc.variables["WITH_OPENGL"] = self.dependencies["mathgl"].options.opengl and \
            not self.dependencies["mathgl"].options.shared and self.settings.os == "Windows"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = path.join(self.cpp.build.bindirs[0], "example")
            self.run(bin_path, env="conanrun")

            if self.dependencies["mathgl"].options.qt5:
                bin_path = path.join(self.cpp.build.bindirs[0], "qt_example")

                self.run(bin_path + " -platform offscreen", env="conanrun")
