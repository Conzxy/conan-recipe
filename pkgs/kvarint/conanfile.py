from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get
from conan.tools.scm import Git

class kvarintRecipe(ConanFile):
    name = "kvarint"
    version = "1.0"

    # Optional metadata
    license = "MIT"
    author = "Conzxy zengxiaoyu0@gmail.com"
    url = "https://github.com/Conzxy/kvarint"
    description = "A C implementation of varint compression algorithm from google"
    topics = ("serialization", "algorithm", "encoder", "decoder", "bits", "byte-order", "compression-algorithm", "big-endian", "varints")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    #exports_sources = "CMakeLists.txt", "src/*", "include/*"
    
    def source(self):
        git = Git(self)
        git.clone(url=self.url, target='.')

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["kvarint"]
