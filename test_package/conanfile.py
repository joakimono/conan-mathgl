#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
import os


class MathglTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_paths", "cmake_find_package")
    requires = "mathgl/[>=2.44]"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["WITH_QT"] = self.options["mathgl"].qt5
        cmake.configure()
        cmake.build()

    def imports(self):
        if self.settings.os == "Windows":
            self.copy("*.dll", dst=str(self.settings.build_type),
                      keep_path=False)

    def test(self):
        program = 'example'
        if self.settings.os == "Windows":
            program += '.exe'
            test_path = os.path.join(str(self.build_folder),
                                     str(self.settings.build_type))
        else:
            test_path = '.' + os.sep
        self.run(os.path.join(test_path, program))

        if self.options['mathgl'].qt5:
            program = 'qt_example'
            if self.settings.os == "Windows":
                program += '.exe'
                test_path = os.path.join(str(self.build_folder),
                                         str(self.settings.build_type))
            else:
                test_path = '.' + os.sep
            self.run(os.path.join(test_path, program))
