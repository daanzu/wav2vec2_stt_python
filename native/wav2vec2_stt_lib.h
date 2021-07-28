//
// This file is part of wav2vec2_stt.
// (c) Copyright 2021 by David Zurow
// Licensed under the AGPL-3.0; see LICENSE file.
//

#pragma once

#if defined(_MSC_VER)
    #ifdef WAV2VEC2_STT_EXPORTS
        #define WAV2VEC2_STT_API extern "C" __declspec(dllexport)
    #else
        #define WAV2VEC2_STT_API extern "C" __declspec(dllimport)
    #endif
#elif defined(__GNUC__)
    // unnecessary
    #define WAV2VEC2_STT_API extern "C" __attribute__((visibility("default")))
#else
    #define WAV2VEC2_STT_API
    #pragma warning Unknown dynamic link import / export semantics.
#endif

#include <cstdint>

WAV2VEC2_STT_API bool wav2vec2_stt__init(const char *model_dirname);
WAV2VEC2_STT_API bool wav2vec2_stt__decode(float *wav_samples, int32_t wav_samples_len, char *text, int32_t text_max_len);
