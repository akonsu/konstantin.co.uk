// -*-actionscript-*- Time-stamp: <player.as - root>
// copyright (c) konstantin.co.uk. all rights reserved.

package
{
    import flash.display.*;
    import flash.events.*;
    import flash.media.*;
    import flash.net.*;
    import flash.text.*;

    import button;

    public class player extends Sprite
    {
        private var _button_play:button;
        private var _button_stop:button;
        private var _channel:SoundChannel;
        private var _label:TextField;
        private var _sound:Sound;

        private function button_play_on_click(e:MouseEvent):void
        {
            if (_button_play && _button_stop && !_channel && _sound)
            {
                    _button_play.enabled = false;
                    _button_stop.enabled = !_button_play.enabled;
                    _channel = _sound.play();
                    _channel.addEventListener(Event.SOUND_COMPLETE, channel_on_sound_complete);
            }
        }

        private function button_stop_on_click(e:MouseEvent):void
        {
            if (_button_play && _button_stop && _channel)
            {
                _button_play.enabled = true;
                _button_stop.enabled = !_button_play.enabled;
                _channel.stop();
                _channel = null;
            }
        }

        private function channel_on_sound_complete(e:Event):void
        {
            if (_button_play && _button_stop)
            {
                _button_play.enabled = true;
                _button_stop.enabled = !_button_play.enabled;
                _channel = null;
            }
        }

        private function sound_on_complete(e:Event):void
        {
            if (_label)
            {
                try
                {
                    removeChild(_label);
                }
                catch (error:ArgumentError) {}
            }
        }

        private function sound_on_open(e:Event):void
        {
            var sound:Sound = e.target as Sound;

            if (sound)
            {
                if (!_button_play)
                {
                    _button_play = new button(button.PLAY);
                    _button_play.addEventListener(MouseEvent.CLICK, button_play_on_click);
                    addChild(_button_play);
                }
                if (!_button_stop)
                {
                    _button_stop = new button(button.STOP);
                    _button_stop.addEventListener(MouseEvent.CLICK, button_stop_on_click);
                    addChild(_button_stop);
                }
                if (!_label)
                {
                    _label = new TextField();
                    _label.autoSize = TextFieldAutoSize.LEFT;
                    _label.background = true;
                    _label.border = false;
                    addChild(_label);
                }
                if (!_sound)
                {
                    _button_play.enabled = true;
                    _button_stop.enabled = !_button_play.enabled;
                    _sound = sound;
                }
                _button_stop.x = 1;
                _button_stop.y = (this.stage.stageHeight - _button_stop.height) / 2;
                _button_play.x = _button_stop.x + _button_stop.width;
                _button_play.y = _button_stop.y;
                _label.x = _button_play.x + _button_play.width;
                _label.y = _button_play.y;
            }
        }

        private function sound_on_progress(e:ProgressEvent):void
        {
            if (_label)
            {
                _label.text = e.bytesLoaded.toString();
            }
        }

        public function player()
        {
            try
            {
                this.stage.align = StageAlign.TOP_LEFT;
                this.stage.scaleMode = StageScaleMode.NO_SCALE;
                this.stage.showDefaultContextMenu = false;

                var sound:Sound = new Sound();

                sound.addEventListener(Event.COMPLETE, sound_on_complete);
                sound.addEventListener(Event.OPEN, sound_on_open);
                sound.addEventListener(ProgressEvent.PROGRESS, sound_on_progress);

                sound.load(new URLRequest(this.root.loaderInfo.parameters.url));
            }
            catch (error:*) {}
        }
    }
}
