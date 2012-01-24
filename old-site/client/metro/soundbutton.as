// -*-actionscript-*- Time-stamp: <soundbutton.as - root>
// copyright (c) 2006-2007 konstantin.co.uk. all rights reserved.

package
{
    import flash.display.*;
    import flash.events.*;
    import flash.media.*;

    public class soundbutton extends Sprite
    {
        private var _cross:Shape;
        private var _frame:Shape;
        private var _symbol:Shape;

        private function on_click(e:MouseEvent):void
        {
            if (_cross)
            {
                var transform:SoundTransform = SoundMixer.soundTransform;

                _cross.visible = !_cross.visible;
                transform.volume = _cross.visible ? 0 : 1;
                SoundMixer.soundTransform = transform;
            }
        }

        private function on_mouseout(e:MouseEvent):void
        {
            if (_frame)
            {
                _frame.visible = false;
            }
        }

        private function on_mouseover(e:MouseEvent):void
        {
            if (_frame)
            {
                _frame.visible = true;
            }
        }

        public function soundbutton()
        {
            const SIZE:int = 25;

            var x:int = 8;
            var y:int = Math.round(SIZE / 2);

            var dx:int = 3;
            var dy:int = 3;

            _cross = new Shape();
            _frame = new Shape();
            _symbol = new Shape();

            _cross.visible = false;
            _frame.visible = false;

            buttonMode = true;

            with (_cross.graphics)
            {
                clear();
                lineStyle(1);

                moveTo(0, 0); lineTo(SIZE + 1, SIZE + 1);
                moveTo(0, SIZE + 1); lineTo(SIZE + 1, 0);
            }
            with (_frame.graphics)
            {
                clear();
                lineStyle(2);

                drawRect(0, 0, SIZE + 1, SIZE + 1);
            }
            with (_symbol.graphics)
            {
                clear();
                lineStyle(1);

                beginFill(0xffffff);
                drawRect(0, 0, SIZE, SIZE);
                endFill();

                for (var i:int = 1; i < 4; i++)
                {
                    moveTo(x + i * dx, y - i * dy);
                    curveTo(x + i * (dx + 2), y, x + i * dx, y + i * dy);
                }
                drawRect(x - 2, y - 1, 2, 2);
            }
            addChild(_symbol);
            addChild(_frame);
            addChild(_cross);

            addEventListener(MouseEvent.CLICK, on_click);
            addEventListener(MouseEvent.MOUSE_OUT, on_mouseout);
            addEventListener(MouseEvent.MOUSE_OVER, on_mouseover);
        }
    }
}
