# Explain Vulkan


#### **Abstract Level of Vulkan**
 - Global-level functions. Allow us to create a Vulkan instance.
 - Instance-level functions. Check what Vulkan-capable hardware is available and what Vulkan features are exposed.
 - Device-level functions. Responsible for performing jobs typically done in a 3D application (like drawing).

#### **Import Vulkan**, see [here](https://www.intel.com/content/www/us/en/developer/articles/training/api-without-secrets-introduction-to-vulkan-part-1.html)

Three way to choose:

1. Dynamically load the driver’s library that provides Vulkan API implementation and acquire function pointers by ourselves from it. (NOT recommended, due to hardware vendors can modify their drivers in any way, and it may affect compatibility with a given application.)
2. Use the Vulkan SDK and link with the provided Vulkan Runtime (Vulkan Loader) static library.
3. Use the Vulkan SDK, dynamically load Vulkan Loader library at runtime, and load function pointers from it. (adopted by volk, a meta loader for Vulkan API, see https://github.com/zeux/volk)

This choice whether static or runtime link is just a matter of personal preference.

To import Vulkan at runtime:

- Step 1: import `vkGetInstanceProcAddr()` by OS-specific interfaces
- Step 2: import all global-level functions by `vkGetInstanceProcAddr(nullptr, func_name)`
- Step 3: import all instance-level functions by `vkGetInstanceProcAddr(vkInstance, func_name)`

#### **Extension**
**additional functionality that is not required by core specifications, and not all hardware vendors may implement them, like layers**. Extensions are also divided into instance and device levels, and extensions from different levels must be enabled separately.

#### **Feature**

**additional hardware capabilities that are similar to extensions.** Features  may not necessarily be supported by the driver and by default are not enabled. If a given physical device supports any feature we can enable it during logical device creation. e.g., geometry shaders.

A logical device represents a physical device and all the features and extensions we enabled for it.

#### **Suffixes of Extension**,  see [here](https://www.reddit.com/r/vulkan/comments/9twibs/what_are_these_2khr_things/)  
- *KHR: every Vulkan extension entity has a suffix (e.g., EXT, NV, AMD). KHR means Khronos extension, and many KHR were promoted to newer Vulkan version, which means there may as well be the same entities without the suffix.
    
- *2: (and possibly 3, 4, ...) is used because the original name is already taken. Typically done for improvements of the original function as newer version, or fixing defects. E.g. some *2 structures add pNext (which the original was missing) in order for them to be extensible.

Thus, For the functions and types of the same name in the latest version of Vulkan, it is preferred to choose the one without the extension suffix and the one with a larger suffix number, which can obtain the best functionality.

#### **Layout**
**layout, is an internal memory arrangement of an image.** Image data may be organized in such a way that neighboring “image pixels” are also neighbors in memory, which can increase cache hits (faster memory reading) when image is used as a source of data (that is, during texture sampling). But caching is not necessary when the image is used as a target for drawing operations, and the memory for that image may be organized in a totally different way. Image may have linear layout (which gives the CPU ability to read or populate image’s memory contents) or optimal layout (which is optimized for performance but is also hardware/vendor dependent). So some hardware may have special memory organization for some types of operations; other hardware may be operations-agnostic. Some of the memory layouts may be better suited for some intended image “usages.” Or from the other side, some usages may require specific memory layouts. There is also a general layout that is compatible with all types of operations. But from the performance point of view, it is always best to set the layout appropriate for an intended image usage and it is application’s responsibility to inform the driver about transitions. Usually, we may change  image layouts  by using image memory barriers manually or by  the hardware inside a render pass automatically.
