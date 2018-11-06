from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, check_sha1
import os, shutil


class MsqlitecppConan(ConanFile):
    name = "mSqliteCpp"
    version = "0.9.1"
    license = "MIT"
    author = "Federico Fuga <fuga@studiofuga.com>"
    url = "https://github.com/studiofuga/mSqliteCpp"
    description = "A Modern C++ sqlite interface implementation"
    topics = ("sqlite", "c++14")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "boost/1.66.0@conan/stable"

    def source(self):
        self.run("git clone https://github.com/studiofuga/mSqliteCpp.git")
        self.run("cd mSqliteCpp && git checkout master")
        # Download sqlite amalgamation
        zip_name = "sqlite-amalgamation-3250300.zip"
        download("http://www.sqlite.org/2018/%s" % zip_name, zip_name)
        check_sha1(zip_name, "b78c2cb0d2c9182686c582312479f96a82bf5380")
        unzip(zip_name, "mSqliteCpp")
        try:
            os.chdir("mSqliteCpp")
            os.rename("sqlite-amalgamation-3250300", "sqlite-amalgamation")
        finally:
            os.chdir("..")
        os.unlink(zip_name)

    def configure_cmake(self):
        cmake = CMake(self)
        d = {"WITH_CONAN": "ON",
             "ENABLE_TEST": "OFF",
             "ENABLE_PROFILER": "OFF",
             "ENABLE_SQLITE_AMALGAMATION": "ON"}
        cmake.configure(source_folder="mSqliteCpp", defs=d)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        """
        self.copy("*.h", dst="include", src="include")
        self.copy("*msqlitecpp.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        """

    def package_info(self):
        self.cpp_info.libs = ["mSqliteCpp"]

