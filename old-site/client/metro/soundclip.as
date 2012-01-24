// -*-actionscript-*- Time-stamp: <soundclip.as - root>
// copyright (c) 2006-2007 konstantin.co.uk. all rights reserved.

package
{
    import flash.events.*;
    import flash.media.*;

    public class soundclip extends EventDispatcher
    {
        private static const FADE_INTERVAL:Number = 5000;

        public static const SOUND_FADE:String = "SOUND_FADE";

        private var _channel:SoundChannel;
        private var _complete:Boolean;
        private var _p0:Number;
        private var _p1:Number;

        private function on_enterframe(e:Event):void
        {
            if (_channel)
            {
                var transform:SoundTransform = _channel.soundTransform;

                if (_p1 < _channel.position)
                {
                    if (!_complete)
                    {
                        _complete = true;
                        dispatchEvent(new Event(SOUND_FADE));
                    }
                    if (transform.volume > 0)
                    {
                        transform.volume = Math.max(0, Math.min(1, (_p1 - _channel.position + FADE_INTERVAL) / FADE_INTERVAL));
                        _channel.soundTransform = transform;
                    }
                    else
                    {
                        _channel.stop();
                        dispatchEvent(new Event(Event.SOUND_COMPLETE));
                        removeEventListener(Event.ENTER_FRAME, on_enterframe);
                    }
                }
                else if (transform.volume < 1)
                {
                    transform.volume = Math.max(0, Math.min(1, (_channel.position - _p0 + FADE_INTERVAL) / FADE_INTERVAL));
                    _channel.soundTransform = transform;
                }
            }
        }

        public function soundclip(sound:Sound)
        {
            var extent:Number = sound.length - 2 * FADE_INTERVAL;

            if (extent > 0)
            {
                var p0:Number = FADE_INTERVAL + Math.random() * extent;
                var p1:Number = FADE_INTERVAL + Math.random() * extent;

                _p0 = Math.min(p0, p1);
                _p1 = Math.max(p0, p1);

                _channel = sound.play(_p0 - FADE_INTERVAL, 0, new SoundTransform(0));
                addEventListener(Event.ENTER_FRAME, on_enterframe);
            }
            else
            {
                const f:Function = function(e:Event):void
                    {
                        dispatchEvent(new Event(SOUND_FADE));
                        dispatchEvent(e.clone());
                    }
                _channel = sound.play();
                _channel.addEventListener(Event.SOUND_COMPLETE, f);
            }
        }
    }
}
