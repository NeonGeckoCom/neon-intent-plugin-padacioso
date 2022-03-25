#!/usr/bin/env python3
from setuptools import setup

PLUGIN_ENTRY_POINT = 'neon-intent-plugin-padacioso=neon_intent_plugin_padacioso:PadaciosoExtractor'
setup(
    name='neon-intent-plugin-padacioso',
    version='0.0.1',
    description='A intent plugin for mycroft',
    url='https://github.com/NeonGeckoCom/neon-intent-plugin-padacioso',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['neon_intent_plugin_padacioso'],
    install_requires=["ovos-plugin-manager", "padacioso"],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={'intentbox.intent': PLUGIN_ENTRY_POINT}
)
