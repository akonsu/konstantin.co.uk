// -*-actionscript-*- Time-stamp: <metro.as - root>
// copyright (c) 2006-2007 konstantin.co.uk. all rights reserved.

package
{
    import flash.display.*;
    import flash.events.*;
    import flash.net.*;

    import soundbox;
    import soundbutton;
    import soundclip;

    public class metro extends Sprite
    {
        private const BUTTON_MARGIN:int = 2;

        [Embed(source="metro.svg")]
        private var SVG:Class;

        private var _box:soundbox;
        private var _button:soundbutton;

        private function sprite_scale(sprite:Sprite):void
        {
            if (sprite)
            {
                with (sprite)
                {
                    var D:int = _button.width + BUTTON_MARGIN * 2;
                    var w:int = width;
                    var h:int = height;
                    var W:int = this.stage.stageWidth - D;
                    var H:int = this.stage.stageHeight;

                    if (W * h > H * w)
                    {
                        height = H;
                        width = w * H / h;
                        x = D + (W - width) / 2;
                        y = 0;
                    }
                    else
                    {
                        height = h * W / w;
                        width = W;
                        x = D;
                        y = (H - height) / 2;
                    }
                }
            }
        }

        public function metro()
        {
            try
            {
                var sprite:Sprite = new SVG();
                var urls:String = root.loaderInfo.parameters.urls;

                stage.align = StageAlign.TOP_LEFT;
                stage.scaleMode = StageScaleMode.NO_SCALE;
                stage.showDefaultContextMenu = false;

                _box = new soundbox(urls ? urls.split('|') : null);
                _button = new soundbutton();

                sprite_scale(sprite);

                _button.x = _button.y = BUTTON_MARGIN;

                addChild(_button);
                addChild(sprite);
            }
            catch (error:*) {}
        }
    }
}
