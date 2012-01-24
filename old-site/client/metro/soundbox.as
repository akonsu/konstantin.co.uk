// -*-actionscript-*- Time-stamp: <soundbox.as - root>
// copyright (c) 2006-2007 konstantin.co.uk. all rights reserved.

package
{
    import flash.display.*;
    import flash.events.*;
    import flash.media.*;
    import flash.net.*;

    public class soundbox extends Sprite
    {
        private var _busy:Boolean = false;
        private var _clips:Array = [];
        private var _recycle:Boolean = false;
        private var _sounds:Array = [];

        private function sound_on_complete(e:Event):void
        {
            var sound:Sound = e.target as Sound;

            if (sound)
            {
                _sounds.push(sound);
            }
        }

        private function on_enterframe(e:Event):void
        {
            if (!_busy && _sounds.length > 0)
            {
                var sound:Sound = _sounds[Math.floor(Math.random() * _sounds.length)];
                var clip:soundclip = new soundclip(sound);

                _busy = true;
                _clips.push(clip);

                clip.addEventListener(Event.SOUND_COMPLETE, on_soundcomplete);
                clip.addEventListener(soundclip.SOUND_FADE, function (e:Event):void { _busy = false });
            }
            if (_recycle)
            {
                _clips = _clips.filter(function (x:*, i:int, array:Array):Boolean { return x != null });
                _recycle = false;
            }
            _clips.forEach(function (x:*, i:int, array:Array):void { x.dispatchEvent(e.clone()) });
        }

        private function on_soundcomplete(e:Event):void
        {
            var i:int = _clips.indexOf(e.target);

            if (0 <= i && i < _clips.length)
            {
                _clips[i] = null;
                _recycle = true;
            }
        }

        public function soundbox(params:Array)
        {
            if (params && params.length > 0)
            {
                while (params.length > 0)
                {
                    var sound:Sound = new Sound();
                    var urls:Array = params.splice(Math.floor(Math.random() * params.length), 1);

                    sound.addEventListener(Event.COMPLETE, sound_on_complete);
                    sound.load(new URLRequest(urls[0]));
                }
                addEventListener(Event.ENTER_FRAME, on_enterframe);
            }
        }
    }
}
