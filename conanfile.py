import shutil
from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
import os


class LIBJPEGTURBOConan(ConanFile):
    name = "libjpeg_turbo"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    generators = "CMakeDeps"

    def requirements(self):
        self.requires(f"zlib/{self.version}")

    def export_sources(self):
        conan.tools.files.copy(self, "*", self.recipe_folder, self.export_sources_folder)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["WITH_TURBOJPEG"] = False
        tc.variables["ENABLE_STATIC"] = not self.options.shared
        tc.variables["ENABLE_SHARED"] = self.options.shared
        tc.generate()

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs.append("cmake")
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake"))
