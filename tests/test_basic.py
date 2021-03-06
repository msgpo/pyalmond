# Copyright 2019 The Board of Trustees of the Leland Stanford Junior University
#
# Author: Giovanni Campagna <gcampagn@cs.stanford.edu>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import aiohttp
from pyalmond import WebAlmondAPI, AlmondLocalAuth

import pytest


@pytest.mark.asyncio
async def test_simple():
    async with aiohttp.ClientSession() as client:
        auth = AlmondLocalAuth('http://127.0.0.1:3000', client)
        almond_api = WebAlmondAPI(auth)

        # issue the first command and discard the result (this will cause
        # Almond to spew the welcome messages)
        await almond_api.async_converse_text("hello")

        result = await almond_api.async_converse_text("hello")
        assert result == {
            "askSpecial": None,
            "messages": [{
                "type": "text",
                "text": "Hi!",
                "icon": None
            }],
            "conversationId": "stateless"
        }


@pytest.mark.asyncio
async def test_apps():
    async with aiohttp.ClientSession() as client:
        auth = AlmondLocalAuth('http://127.0.0.1:3000', client)
        almond_api = WebAlmondAPI(auth)

        assert await almond_api.async_list_apps() == []


@pytest.mark.asyncio
async def test_devices():
    async with aiohttp.ClientSession() as client:
        auth = AlmondLocalAuth('http://127.0.0.1:3000', client)
        almond_api = WebAlmondAPI(auth)

        await almond_api.async_create_simple_device('com.xkcd')

        devices = await almond_api.async_list_devices()
        assert any(d['kind'] == 'com.xkcd' for d in devices)
