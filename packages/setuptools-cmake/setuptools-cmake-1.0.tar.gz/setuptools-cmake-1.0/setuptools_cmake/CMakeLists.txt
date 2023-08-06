# This version is needed for the below function to work
cmake_minimum_required(VERSION 3.11)

# PyBind11 support -------------------------------------------------------
# This function changes the way `find_package()` results are saved. Usually,
# they are saved only for the current CMakeLists.txt, which means, that in
# our case, `pybind11` would not be imported for any projects which include
# this file. Therfore, we change `IMPORTED` to `IMPORTED_GLOBAL`, so that
# upstream config files can also access the packages found by this file.
function(add_library)
    set(_args ${ARGN})
    if ("${_args}" MATCHES ";IMPORTED")
        list(APPEND _args GLOBAL)
    endif()
    _add_library(${_args})
endfunction()
find_package(pybind11 REQUIRED)

# Quick function for adding Python submodules via PyBind11, based on
# https://gist.github.com/hovren/5b62175731433c741d07ee6f482e2936
function(python_module module type)
    set(target_name ${module})
    string(REPLACE "." "/" modpath ${module})
    string(REPLACE "." ";" modlist ${module})

    # The module name is the last entry
    list(GET modlist -1 modname)

    # Remove everything that is not the root or the module name
    #list(REMOVE_AT modlist 0)
    list(REMOVE_AT modlist -1)

    # Get the relative path
    if(modlist)
        string(REPLACE ";" "/" relpath "${modlist}")
    else()
        set(relpath "")
    endif()

    # Define the binding source file
    set(sources ${relpath}/${modname}.${type})

    # Invoke pybind11 and set where the library should go, and what it is called
    pybind11_add_module(${target_name} ${sources})
    
    set(outdir ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${relpath})

    message(info " " ${module} " " ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${relpath})
    message(info " " ${module} " " ${outdir})

    # target_include_directories(${target_name} PUBLIC lib/pybind11/include)
    set_target_properties(${target_name} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${outdir}$<0:>)
    set_target_properties(${target_name} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${outdir})
    set_target_properties(${target_name} PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${outdir})
    set_target_properties(${target_name} PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${outdir})
    set_target_properties(${target_name} PROPERTIES OUTPUT_NAME ${modname})
endfunction()
