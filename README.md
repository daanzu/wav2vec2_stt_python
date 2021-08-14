# Wav2Vec2 STT Python

> **Beta Software**

> Simple Python library, distributed via binary wheels with few direct dependencies, for easily using [wav2vec 2.0](https://github.com/pytorch/fairseq/blob/master/examples/wav2vec/README.md) models for speech recognition.

[![Donate](https://img.shields.io/badge/donate-GitHub-pink.svg)](https://github.com/sponsors/daanzu)
[![Donate](https://img.shields.io/badge/donate-Patreon-orange.svg)](https://www.patreon.com/daanzu)
[![Donate](https://img.shields.io/badge/donate-PayPal-green.svg)](https://paypal.me/daanzu)

Requirements:
* Python 3.7+
* Platform: Linux x64 (Windows is a work in progress; MacOS may work; PRs welcome)
* Python package requirements: `cffi`, `numpy`
* Wav2Vec2 2.0 Model (must be converted to compatible format)
    * Several are available ready-to-go on this project's [releases page](https://github.com/daanzu/wav2vec2_stt_python/releases) and below.
    * You can convert your own models by following the instructions [here](https://github.com/pytorch/audio/blob/master/examples/libtorchaudio/speech_recognition/README.md).

Models:

| Model | Download Size |
|--------|--------|
| [Facebook Wav2Vec2 2.0 Base (960h)](https://github.com/daanzu/wav2vec2_stt_python/releases/download/models/facebook_wav2vec2-base-960h.zip) | 360 MB |
| [Facebook Wav2Vec2 2.0 Large (960h)](https://github.com/daanzu/wav2vec2_stt_python/releases/download/models/facebook_wav2vec2-large-960h.zip) | 1.18 GB |
| [Facebook Wav2Vec2 2.0 Large LV60 (960h)](https://github.com/daanzu/wav2vec2_stt_python/releases/download/models/facebook_wav2vec2-large-960h-lv60.zip) | 1.18 GB |
| [Facebook Wav2Vec2 2.0 Large LV60 Self (960h)](https://github.com/daanzu/wav2vec2_stt_python/releases/download/models/facebook_wav2vec2-large-960h-lv60-self.zip) | 1.18 GB |

## Usage

```python
from wav2vec2_stt import Wav2Vec2STT
decoder = Wav2Vec2STT('model_dir')

import wave
wav_file = wave.open('tests/test.wav', 'rb')
wav_samples = wav_file.readframes(wav_file.getnframes())

assert decoder.decode(wav_samples).strip().lower() == 'it depends on the context'
```

## Installation/Building

Recommended installation via wheel from pip (requires a recent version of pip):

```bash
python -m pip install wav2vec2_stt
```

See [setup.py](setup.py) for more details on building it yourself.

## Author

* David Zurow ([@daanzu](https://github.com/daanzu))

## License

This project is licensed under the GNU Affero General Public License v3 (AGPL-3.0-or-later). See the [LICENSE file](LICENSE) for details. If this license is problematic for you, please contact me.

## Acknowledgments

* Contains and uses code from [PyTorch](https://github.com/pytorch/pytorch) and [torchaudio](https://github.com/pytorch/audio), licensed under the BSD 2-Clause License.
