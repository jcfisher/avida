##############################################################################
## Copyright (C) 1999-2006 Michigan State University                        ##
## Based on work Copyright (C) 1993-2003 California Institute of Technology ##
##                                                                          ##
## Read the COPYING and README files, or contact 'avida@alife.org',         ##
## before continuing.  SOME RESTRICTIONS MAY APPLY TO USE OF THIS FILE.     ##
##############################################################################

"""
PlatformTool

Platform-specific initialization for Avida build system.
"""

import SCons
import os
import sys

CLVar = SCons.Util.CLVar

def _posix_defaults(env):
  """
  Default compiler options for posix platforms, assuming they use gcc.
  """
  env.Replace(
    PLATFORM_CPPPATH = CLVar('/usr/include /usr/local/include /opt/local/include' '$CPPPATH'),
    PLATFORM_LIBPATH = CLVar('/usr/lib /usr/local/lib /opt/local/lib' '$LIBPATH'),
    #_PLATFORM_DEBUG_BUILD_FLAGS = "-g $COMPILER_WARNING_FLAGS -pedantic -DDEBUG",
    _PLATFORM_DEBUG_BUILD_FLAGS = "-g $COMPILER_WARNING_FLAGS -DDEBUG",
    _PLATFORM_RELEASE_DEBUG_BUILD_FLAGS = "-O2 -ffast-math -g $COMPILER_WARNING_FLAGS -pedantic -DDEBUG",
    _PLATFORM_RELEASE_BUILD_FLAGS = "-O3 -ffast-math -DNDEBUG",
    _PLATFORM_MINIMUM_RELEASE_BUILD_FLAGS = "-Os -DNDEBUG",
    plat_default_enableTCMalloc = 1,
    plat_default_extrasDir = None,
  )

def darwin_generate(env):
  """
  Compiler and environment tweaks for OS X. Loads posix defaults.
  """
  _posix_defaults(env)
  env.Append(PLATFORM_CPPPATH = CLVar('/sw/include'))
  env.Append(PLATFORM_LIBPATH = CLVar('/sw/lib'))
  env['ENV']['MACOSX_DEPLOYMENT_TARGET'] = '10.4'
  env['ENV']['GCCXML_COMPILER'] = 'c++-3.3'

  env.Replace(
    COMPILER_WARNING_FLAGS = "-Wall -Wno-long-double -Wno-long-long",
    plat_default_enableMemTracking = 0,
    plat_default_enablePyPkg = 0,
    plat_default_enableSerialization = 0,
    plat_default_enableSharedPtr = 0,
    plat_default_pythonCommand = sys.executable,
    plat_default_boostIncludeDir = None,
    plat_default_boostPythonLibDir = None,
    plat_default_boostPythonLib = None,
    plat_default_GccXmlCommand = None,
    plat_default_pysteScriptPath = os.path.join(sys.path[0], '${AvidaUtils_path}', 'AvidaPyste.py'),
    plat_default_pysteScriptCommand = SCons.Util.CLVar('$pythonCommand $pysteScriptPath'),
  )

def linux_generate(env):
  _posix_defaults(env)

def cygwin_generate(env):
  _posix_defaults(env)

def win32_generate(env):
  """
  Options for Visual Studio's compiler.
  """
# Visual Studio's compiler options:
#
# General:
#   Additional Include Directories:
#   * Specifies one or more directories to add to the include path; use
#     semi-colon delimited list if more than one.
#   - (/I[path])
#   Debug Information Format:
#   * Specifies the type of debugging information generated by the compiler.
#     You must also change linker settings appropriately to match.
#   - Disabled
#   - C7 Compatible (/Z7)
#   - Line Numbers Only (/Zd)
#   - Program Database (/Zi)
#   - Program Database for Edit & Continue (/ZI)
#   Compile As Managed:
#   * Use the .NET runtime services. Incompatible with any runtime checks.
#   - Not using managed extensions
#   - Assembly Support (/clr)
#   Supress Startup Banner:
#   * Suppress the display of the startup banner and information messages.
#   - No
#   - Yes (/nologo)
#   Warning Level:
#   * Select how strict you want the compiler to be about checking for
#     potentially suspect constructs.
#   - Off: Turn Off All Warnings (/W0)
#   - Level 1 (/W1)
#   - Level 2 (/W2)
#   - Level 3 (/W3)
#   - Level 4 (/W4)
#   Detect 64-bit Portability Issues:
#   - No
#   - Yes (/Wp64)
#   Treat Warnings As Errors:
#   - No
#   - Yes (/WX)
#
# Optimization:
#   Optimization:
#   - Disabled (/Od)
#   - Minimum Size (/O1)
#   - Maximum Speed (/O2)
#   - Full Optimization (/Ox)
#   Global Optimization:
#   * Enables global optimizations; incompatible with all 'Runtime Checks'
#     options and edit and continue.
#   - No
#   - Yes (/Og)
#   Inline Function Expansion:
#   - Default
#   - Only __inline (/Ob1)
#   - Any Suitable (/Ob2)
#   Enable Intrinsic Functions:
#   * Using intrinsic functions generates faster but possibly larger code.
#   - No
#   - Yes (/Oi)
#   Floating Point Consistency:
#   * Enables improving floating-point consistency during calculations.
#   - Default Consistency
#   - Improved Consistency (/Op)
#   Favor Size or Speed:
#   * Choose whether to favor code size or code speed; 'Global Optimization'
#     must be turned on.
#   - Neither
#   - Favor Fast Code (/Ot)
#   - Favor Small Code (/Os)
#   Omit Frame Pointers:
#   * Suppresses frame pointers.
#   - No
#   - Yes (/Oy)
#   Enable Fiber-safe Optimizations:
#   * Enables memory space optimization when using fibers and thread local
#     storage access.
#   - No
#   - Yes (/GT)
#   Optimize For Processor:
#   * Optimize code to favor a specific X86 processor; use Blended to work best
#     across all processors.
#   - Blended
#   - Pentium (/G5)
#   - Pentium Pro, Pentium II, Pentium III (/G6)
#   - Pentium 4 and Above (/G7)
#   Optimize For Windows Application:
#   * Specify whether to optimize code in favor of windows .EXE execuation.
#   - No
#   - Yes (/GA)
#
# Preprocessor:
#   Preprocessor Definitions:
#   * Specifies one or more preprocessor defines.
#   - (/D[macro])
#   Ignore Standard Include Path:
#   - No
#   - Yes (/X)
#   Generate Preprocessed Files:
#   - No
#   - With Line Numbers (/P)
#   - Without Line Numbers (/EP /P)
#   Keep Comments:
#   * Suppresses comment strip from source code; requires that one of the
#     'Preprocessing' options be set.
#   - No
#   - Yes (/C)
#
# Code Generation:
#   Enable String Pooling:
#   * Enable read-only string pooling for generating smaller compiled code.
#   - No
#   - Yes (/GF)
#   Enable Minimal Rebuild:
#   * Detect changes to C++ class definitions and recompile only affected
#   source files.
#   - No
#   - Yes (/Gm)
#   Enable C++ Exceptions:
#   * Calls destructors for automatic objects during a stack unwind caused by
#     an exception being thrown.
#   - No
#   - Yes /EHsc
#   Smaller Type Check
#   * Enable checking for conversion to smaller types; incompatible with any
#     optimization type other than debug.
#   - No
#   - Yes (/RTCc)
#   Basic Runtime Checks:
#   * Perform basic runtime error checks, incompatible with any optimization
#     type other than debug.
#   - Default
#   - Stack Frames (/RTCs)
#   - Uninitialized Variables (/RTCu)
#   - Both (/RTC1, equivalent to /RTCsu)
#   Runtime Library:
#   * Specify runtime library for linking.
#   - Multi-threaded (/MT)
#   - Multi-threaded Debug (/MTd)
#   - Multi-threaded DLL (/MD)
#   - Multi-threaded Debug DLL (/MDd)
#   - Single-threaded (/ML)
#   - Single-threaded Debug (/MLd)
#   Struct Member Alighment:
#   * Specify 1, 2, 4, 8, or 16-byte boundaries for struct member alignment.
#   - Default
#   - num (/Zp[num]
#   Buffer Security Check:
#   * Check for buffer overruns; useful for closing hackable loopholes on
#     internet servers; ignored for projects using managed extensions.
#   - No
#   - Yes (/GS)
#   Enable Function-Level Linking:
#   * Required for Edit and Continue to work.
#   - No
#   - Yes (/Gy)
#   Enable Enhanced Instruction Set:
#   * Enable use of instructions found on processors that support enhanced
#     instruction sets, e.g., the SSE and SSE2 enhancements to the IA-32.
#   - Not Set
#   - Streaming SIMD Extensions (/arch:SSE)
#   - Streaming SIMD Extensions 2 (/arch:SSE2)
#
# Language:
#   Disable Language Extensions:
#   - No
#   - Yes (/Za)
#   Default Char Unsigned:
#   * Sets the default char type to unsigned.
#   - No
#   - Yes (/J)
#   Treat wchar_t as Built-in Type:
#   - No
#   - Yes (/Zc:whar_t)
#   Force Conformance In For Loop Scope:
#   * Forces the compiler to conform to the local scope in a for loop.
#   - No
#   - Yes (/Zc:forScope)
#   Enable Run-Time Type Info:
#   * Adds code for checking C++ objects types at run time (runtime type
#     information.
#   - No
#   - Yes (/GR)
#
# Precompiled Headers
#   Create / Use Precompiled Header:
#   * Enables creation or use of a precompiled header during the build.
#   - Not Using Precompiled Headers
#   - Create Precompiled Header (/Yc)
#   - Automatically generate (/YX)
#   - Use Precompiled Header (/Yu)
#   Create / Use PCH THrough File:
#   * Specifies header file name to use when creating or using a precompiled
#   header file.
#   - (/Yc[name], /YX[name], /Yu[name])
#   Precompiled Header File:
#   * Specifies the path and / or name of the generated header file.
#   - (/Fp[name])
#
# Output Files
#   Expand Attributed Source:
#   * Create listing file with expanded attributes injected into source file.
#   - No
#   - Yes (/Fx)
#   Assembler Output:
#   * Specifies the contents of assembly language output file.
#   - No Listing
#   - Assembly-only Listing (/FA)
#   - Assembly, Machine Code, and Source (/FAcs)
#   - Assembly with Machine Code (/FAs)
#   - Assembly with Source Code (/FAs)
#   ASM List Location:
#   * Specifies relative path and/or name for ASM listing file; can be file or
#     directory name.
#   - (/Fa[name])
#   Object File Name:
#   * Specifies a name to override the default object file name; can be file or
#     directory name.
#   - (/Fo[name])
#   Program Database File Name:
#   * Specifies a name for a compiler-generated PDB file; also specifies base
#     name for the required compiler-generated IDB file; can be file or
#     directory name.
#   - (/Fd[name]
#
# Browse Information
#   Enable Browse Information:
#   * Specifies level of browse information in .bsc file\
#   - None
#   - Include All Browse Information (/FR)
#   - No local symbols (/Fr)
#   Browse File:
#   * Specifies optional name for browser information file.
#   - (/Fr[name], /FR[name])
#
# Advanced
#   Calling Convention:
#   * Select the default calling convention for your application (can be
#     overriden by function).
#   - __cdecl (/Gd)
#   - __fastcall (/Gr)
#   - __stdcall (/Gz)
#   Compile as:
#   * Select compile language option for .c and .cpp files.
#   - Default
#   - Compile as C code (/TC)
#   - Compile as C++ code (/TP
#   Disable Specific Warnings:
#   * Disable the desired warning numbers; put numbers in a semi-colon
#     delimited list.
#   - (/wd<num>)
#   Force Includes:
#   * Specifies one or more forced include files.
#   - (/FI[name])
#   Force #using
#   * Specifies one or more forced #using files.
#   - (/FU[name])
#   Show Includes:
#   * Generates a list of include files with the compiler output.
#   - No
#   - Yes (/showIncludes)
#   Undefine Preprocessor Definitions:
#   * Specifies one or more preprocessor undefines.
#   - (/U[macro])
#   Undefine All Preprocessor Definitions:
#   - No
#   - Yes (/u)

  env.Replace(
    _PLATFORM_DEBUG_BUILD_FLAGS = '/D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_MBCS" /FD /EHsc /RTCs /MDd /GS /GR /W3 /nologo /c /Zi /TP /Zm1000',
    _PLATFORM_RELEASE_DEBUG_BUILD_FLAGS = '/D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_MBCS" /O1 /EHsc /MD /W3 /nologo /c /Zi /TP /Zm1000',

    _PLATFORM_RELEASE_BUILD_FLAGS = '/D "WIN32" /D "_WINDOWS" /D "_MBCS" /O2 /EHsc /MD /W3 /nologo /c /TP /Zm1000 /D NDEBUG',
    _PLATFORM_MINIMUM_RELEASE_BUILD_FLAGS = '/D "WIN32" /D "_WINDOWS" /D "_MBCS" /O1 /EHsc /MD /W3 /nologo /c /TP /Zm1000 /D NDEBUG',
  )

  # pthread's not available on Windows; This points to Dave's workaround, a
  # header file with a null pthread implementation.
  env.Append(CPPPATH = ['#/source/platform/win32-pthread'])

  env.Replace(
    plat_default_enableMemTracking = 0,
    plat_default_enablePyPkg = 0,
    plat_default_enableSerialization = 0,
    plat_default_enableSharedPtr = 0,
    plat_default_enableTCMalloc = 0,
    plat_default_extrasDir = None,
    plat_default_pythonCommand = sys.executable,
    plat_default_boostIncludeDir = None,
    plat_default_boostPythonLibDir = None,
    plat_default_boostPythonLib = None,
    plat_default_GccXmlCommand = None,
    plat_default_pysteScriptPath = os.path.join(sys.path[0], '${AvidaUtils_path}', 'AvidaPyste.py'),
    plat_default_pysteScriptCommand = SCons.Util.CLVar('$pythonCommand $pysteScriptPath'),
  )


platform_generators = {
  'darwin': darwin_generate,
  'linux': linux_generate,
  'cygwin': cygwin_generate,
  'win32': win32_generate,
}

def generate(env):
  """
  Selects compiler and environment options based on platform name.
  """
  # PLATFORM_TOOL_ERR is used to report messages back to the rest of the build
  # system. You can use them as error messages to the user.
  env.Replace(
    PLATFORM_TOOL_ERR = '',
  )
  if env.Dictionary().has_key('PLATFORM'):
    if platform_generators.has_key(env['PLATFORM']):
      platform_generators[env['PLATFORM']](env)
    else:
      env.Append(
        PLATFORM_TOOL_ERR = """
PlatformTool error:
  Platform $$PLATFORM == '%s'
  isn't supported yet.
""" % env['PLATFORM']
      )
  else:
    env.Append(
      PLATFORM_TOOL_ERR = """
PlatformTool error:
  Couldn't obtain $$PLATFORM from environment.
"""
    )
    

def exists(env):
  return True
