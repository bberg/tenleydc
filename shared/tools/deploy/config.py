"""
Configuration for Audio Tools Network deployment
"""

# Site configurations
SITES = {
    "noise-generator": {
        "name": "NoiseGenerator",
        "domain": "focushum.com",
        "local_path": "/Users/bb/www/audio-tools-network/noise-generator",
        "github_repo": "noise-generator",
        "description": "White, pink, brown noise generator for sleep, focus, and relaxation"
    },
    "tone-generator": {
        "name": "ToneGenerator",
        "domain": "tonesynth.com",
        "local_path": "/Users/bb/www/audio-tools-network/tone-generator",
        "github_repo": "tone-generator",
        "description": "Online tone and frequency generator for audio testing"
    },
    "binaural-beats": {
        "name": "BinauralBeats",
        "domain": "binauralhq.com",
        "local_path": "/Users/bb/www/audio-tools-network/binaural-beats",
        "github_repo": "binaural-beats",
        "description": "Binaural beats generator for meditation and focus"
    },
    "drone-generator": {
        "name": "DroneGenerator",
        "domain": "omtones.com",
        "local_path": "/Users/bb/www/audio-tools-network/drone-generator",
        "github_repo": "drone-generator",
        "description": "Ambient drone generator for meditation and yoga"
    },
    "frequency-generator": {
        "name": "FrequencyGenerator",
        "domain": "testtones.com",
        "local_path": "/Users/bb/www/audio-tools-network/frequency-generator",
        "github_repo": "frequency-generator",
        "description": "Precision frequency generator for speaker testing and calibration"
    },
    "metronome": {
        "name": "Metronome",
        "domain": "metronomely.com",
        "local_path": "/Users/bb/www/audio-tools-network/metronome",
        "github_repo": "metronome",
        "description": "Online metronome for musicians"
    }
}

# GitHub organization (set to None for personal repos)
GITHUB_ORG = None  # or "audio-tools-network"

# Network-wide settings
NETWORK_NAME = "Audio Tools Network"
CONTACT_EMAIL = ""  # Set this

# All domains for cross-linking
ALL_DOMAINS = {
    "focushum.com": "Noise Generator",
    "tonesynth.com": "Tone Generator",
    "binauralhq.com": "Binaural Beats",
    "omtones.com": "Drone Generator",
    "testtones.com": "Frequency Generator",
    "metronomely.com": "Metronome"
}
