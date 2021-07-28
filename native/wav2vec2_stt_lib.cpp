//
// This file is part of wav2vec2_stt.
// (c) Copyright 2021 by David Zurow
// Licensed under the AGPL-3.0; see LICENSE file.
//

#include <torch/script.h>

#define BEGIN_INTERFACE_CATCH_HANDLER \
    try {
#define END_INTERFACE_CATCH_HANDLER(expr) \
    } catch(const std::exception& e) { \
        std::cerr << "Trying to survive fatal exception: " << e.what(); \
        return (expr); \
    }

struct Wav2Vec2STTModel {
    Wav2Vec2STTModel(const std::string& model_dirname) {
        try {
            encoder = torch::jit::load(std::string(model_dirname) + "/encoder.zip");
        } catch (const c10::Error &error) {
            std::cerr << "Failed to load the module:" << error.what() << std::endl;
        }
        try {
            decoder = torch::jit::load(std::string(model_dirname) + "/decoder.zip");
        } catch (const c10::Error &error) {
            std::cerr << "Failed to load the module:" << error.what() << std::endl;
        }
    }

    torch::jit::script::Module encoder, decoder;
};

extern "C" {
#include "wav2vec2_stt_lib.h"
}

void *wav2vec2_stt__construct(const char *model_dirname) {
    BEGIN_INTERFACE_CATCH_HANDLER
    auto model = new Wav2Vec2STTModel(model_dirname);
    return model;
    END_INTERFACE_CATCH_HANDLER(nullptr)
}

bool wav2vec2_stt__destruct(void *model_vp) {
    BEGIN_INTERFACE_CATCH_HANDLER
    auto model = static_cast<Wav2Vec2STTModel*>(model_vp);
    delete model;
    return true;
    END_INTERFACE_CATCH_HANDLER(false)
}

bool wav2vec2_stt__decode(void* model_vp, float *wav_samples, int32_t wav_samples_len, char *text, int32_t text_max_len) {
    BEGIN_INTERFACE_CATCH_HANDLER
    auto model = static_cast<Wav2Vec2STTModel*>(model_vp);
    auto options = torch::TensorOptions().dtype(torch::kFloat32);
    auto wav_tensor = torch::from_blob(wav_samples, {1, wav_samples_len}, options);

    auto emission = model->encoder.forward({wav_tensor});
    auto result = model->decoder.forward({emission});

    auto hypothesis = result.toString()->string();
    auto cstr = hypothesis.c_str();
    strncpy(text, cstr, text_max_len);
    text[text_max_len - 1] = 0;  // Just in case.
    return true;
    END_INTERFACE_CATCH_HANDLER(false)
}
