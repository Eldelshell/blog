Date: 2014-04-27
Title: Convert MKV to AVI for Xbox 360 in Linux
Tags: linux
Category: Blog
Slug: xbox-360-mkv-to-avi-linux.md
Author: Eldelshell

For some reason, the Xbox 360 doesn't like Matroska (mkv) files. Basically, `mkv` files are like a
`tar` file with some meta XML, the video file, the different audio files, the different subtitles
and more stuff.

For the Xbox 360 we only care about the video file (track from now on) and the audio file we want
and since everything is already there, inside the `mkv` file, there's really no need to convert
it using __mencoder__ unless the video file is not supported by the Xbox (rarelly happens).

So, first we need to know what we're going to find in the `mkv` file we've legally acquired:

~~~bash
$ mkvinfo 4x02.mkv

+ EBML head
|+ EBML version: 1
|+ EBML read version: 1
|+ EBML maximum ID length: 4
|+ EBML maximum size length: 8
|+ Doc type: matroska
|+ Doc type version: 4
|+ Doc type read version: 2
+ Segment, size 785643352
|+ Seek head (subentries will be skipped)
|+ EbmlVoid (size: 4044)
|+ Segment information
| + Timecode scale: 1000000
| + Muxing application: libebml v1.3.0 + libmatroska v1.4.0
| + Writing application: mkvmerge v6.1.0 ('Old Devil') built on Mar  2 2013 14:32:37
| + Duration: 3152.274s (00:52:32.274)
| + Date: Tue Apr 22 22:56:54 2014 UTC
| + Title: LEGALLY DOWNLOADED FILE
| + Segment UID: 0x8c 0x53 0x7f 0x97 0x08 0x2a 0xda 0x85 0xaa 0x60 0x05 0x0d 0x39 0xab 0x37 0x21
|+ Segment tracks
| + A track
|  + Track number: 1 (track ID for mkvmerge & mkvextract: 0)
|  + Track UID: 721393027
|  + Track type: video
|  + Lacing flag: 0
|  + MinCache: 1
|  + Codec ID: V_MPEG4/ISO/AVC
|  + CodecPrivate, length 44 (h.264 profile: High @L4.1)
|  + Default duration: 41.708ms (23.976 frames/fields per second for a video track)
|  + Language: und
|  + Name: LEGALLY DOWNLOADED FILE
|  + Video track
|   + Pixel width: 1280
|   + Pixel height: 720
|   + Display width: 1280
|   + Display height: 720
| + A track
|  + Track number: 2 (track ID for mkvmerge & mkvextract: 1)
|  + Track type: audio
|  + Codec ID: A_AC3
|  + Default duration: 32.000ms (31.250 frames/fields per second for a video track)
|  + Language: spa
|  + Name: LEGALLY DOWNLOADED FILE
|  + Audio track
|   + Sampling frequency: 48000
|   + Channels: 2
|+ EbmlVoid (size: 1085)
|+ Cluster

~~~

There you can see the information contained in our `mkv` file, the audio and video tracks and more
information about them, like the audio's track language (es) and the ID's which we'll need.

By the way, we need to install __mkvtoolnix__ first <i class="fa fa-smile-o"></i>

Next, we'll extract both files:

~~~bash
$ mkvextract tracks 4x02.mkv 0:4x02.vid
$ mkvextract tracks 4x02.mkv 1:4x02.aud
~~~

Finally, we merge the two together:

~~~bash
$ mkvmerge 4x02.vid 4x02.aud -o 4x02.avi
~~~

And that's it. The great thing about this method instead of using __mencoder__ is that it is _way_ faster and less
error prone than decoding/encoding.
