# conan-recipe

## Introduction
该仓库主要存储我个人所造轮子的[conan](https://github.com/conan-io/conan) recipe。  
其目的是将github作为remote，conan在本地进行包管理。

> 只针对 `conan2`，且只考虑 `CMake` 作为工具链

## Usage
### 安装包
切换到包含 `conanfile.py` 的目录，执行下面命令：
```bash
$ cd kanon/v1.8
$ conan create .
```
这样会将包的`conanfile.py`, `source/`, `package/`等都安装到 **本地缓存(local cache)** 中。
可以配置 `setting` 和 `option` 来进行定制化。比如编译动态库：
```bash
$ conan create . -o shared=True
```
编译Debug版本：
```bash
$ conan create . -s build_type=Debug
```

### 配置本地目录包（编辑模式）
对于自己的轮子（或者一些fork的别人的轮子），往往会有编辑源码的需求，但是如果按照上面的这种做法，会有很多问题：
* 最新的修改并不一定是buf-free的
* 为了让被依赖项目能够使用包，需要提交到remote
* 这个还需要进行新的全量编译，因为修改不稳定，可能需要进行多次

所幸 `conan` 提供了一种方式将特定的目录标记为 **可编辑包（editable packge）**。这种方式虽然也会安装到local cache，但实际会搜索这个目录，通过配置包布局，从而让包用户正确搜索可编辑包的一些路径，达到与本地缓存相同的效果。这种方式往往只需要增量编译，因为本地目录缓存是不需要重新安装的。

> 关于包布局，可以参考 [ConanFile::layout()](https://docs.conan.io/2/tutorial/developing_packages/package_layout.html#developing-packages-layout) 和[templates](templates/)目录文件。

一般是针对最新版本的源码进行修改和提交，因此先拉取源码，再将 `conanfile.py` 拷贝到项目根目录，之后同上。
```bash
$ git clone https://github.com/Conzxy/kanon.git
$ cp */conan-recipe/pkgs/kanon/v1.9.0-pre/conanfile.py kanon/kanon
$ conan editable add kanon
$ cd kanon
$ conan create .
```

### 使用包（消费包）
使用包也需要用户写配置，一般来说，简单的 `conanfile.txt` 就够用了：
```txt
# Example
[requires]
kanon/[>=1.8-]

[options]
kanon*:shared=True

[generators]
CMakeDeps
CMakeToolchain
```
要进行更为灵活和复杂的控制的话，还是得用 `conanfile.py`，在满足 `conanfile.txt` 相同的需求上，还能用 `conan` 提供的API进行编码，具体参考[文档](https://docs.conan.io/2/introduction.html)。   
在编写完配置文件之后，通过 `conan`的命令将必要配置安装到build目录下，然后通过 `*toolchain.cmake` 来设置好一些变量即可：
```bash
$ conan install . -of=build --build=missing
$ cd build
$ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
$ cmake --build . --target [..]
```

## 编写包
参考[templates目录](templates/)下的模板文件以及[文档相关内容](https://docs.conan.io/2/tutorial/creating_packages.html)。
