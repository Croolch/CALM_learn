# mjcf2skeleton

## 介绍

### 1. 创建mesh

方法一： 使用unity打开mjcf文件，然后导出为fbx文件，导入blender

已知问题：model高度不对，需要手动调整

方法二： 使用blender读取mjcf文件，需要开发插件，比较困难的地方在于create geoms

### 2. 创建bones

1. 使用poselib读取mjcf文件，并保存数据为npy文件。这会读取到xml中所有body的name，parent_indices，loacl_translation信息。

2. 使用blender读取npy中的信息，创建bones

### 3. 绑定mesh和bones



## 用法

1. 运行`calm/poselib/save_mjcf_skeleton.py`，生成npy文件，如`armature.npy`

2. blender中运行`blender/generate_armature.py`，生成armature