#
# This file is part of wav2vec2_stt.
# (c) Copyright 2021 by David Zurow
# Licensed under the AGPL-3.0; see LICENSE file.
#

import argparse

from . import _name, Wav2Vec2STT

def main():
    parser = argparse.ArgumentParser(prog='python -m %s' % _name)
    subparsers = parser.add_subparsers(dest='command', help='sub-command')
    decode_parser = subparsers.add_parser('decode', help='decode one or more WAV files')
    decode_parser.add_argument('model', help='Model file to use')
    decode_parser.add_argument('wav_file', nargs='+', help='WAV file to decode')
    args = parser.parse_args()

    if args.command == 'decode':
        import wave
        wav2vec2_stt = Wav2Vec2STT(args.model)
        for wave_file_path in args.wav_file:
            with wave.open(wave_file_path, 'rb') as wav_file:
                wav_data = wav_file.readframes(wav_file.getnframes())
                print(wav2vec2_stt.decode(wav_data))

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
