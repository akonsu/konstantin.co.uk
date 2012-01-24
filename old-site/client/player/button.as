// -*-actionscript-*- Time-stamp: <button.as - root>
// copyright (c) konstantin.co.uk. all rights reserved.

package
{
    import flash.display.*;
    import flash.events.*;
    import flash.media.*;

    public class button extends Sprite
    {
        public static const PLAY:String = "play";
        public static const STOP:String = "stop";

        private var _frame:Shape;
        private var _symbol:Shape;

        private function on_mouseout(e:MouseEvent):void
        {
            if (enabled && _frame)
            {
                _frame.visible = false;
            }
        }

        private function on_mouseover(e:MouseEvent):void
        {
            if (enabled && _frame)
            {
                _frame.visible = true;
            }
        }

        public function get enabled():Boolean
        {
            return this.buttonMode;
        }

        public function set enabled(value:Boolean):void
        {
            if (_frame && !value)
            {
                _frame.visible = false;
            }
            if (_symbol)
            {
                _symbol.alpha = value ? 1.0 : 0.5;
            }
            this.buttonMode = value;
        }

        public function button(type:String)
        {
            const FRAME_SIZE:int = 21;
            const SYM_SIZE:int = FRAME_SIZE - 11;

            _frame = new Shape();
            _symbol = new Shape();

            _frame.visible = false;

            with (_frame.graphics)
            {
                clear();
                lineStyle(2, 0, 1.0, true, LineScaleMode.NORMAL, null, JointStyle.MITER);

                drawRect(0, 0, FRAME_SIZE + 1, FRAME_SIZE + 1);
            }
            with (_symbol.graphics)
            {
                clear();

                beginFill(0xffffff);
                lineStyle(1, 0, 1.0, true, LineScaleMode.NORMAL, null, JointStyle.MITER);
                drawRect(0, 0, FRAME_SIZE, FRAME_SIZE);
                endFill();

                var p:int = Math.round((FRAME_SIZE - SYM_SIZE) / 2);

                beginFill(0);
                lineStyle(undefined, 0, 1.0, true, LineScaleMode.NORMAL, null, JointStyle.MITER);

                switch (type)
                {
                case PLAY:
                    moveTo(p, p); lineTo(p + SYM_SIZE, p + Math.round(SYM_SIZE / 2)); lineTo(p, p + SYM_SIZE); lineTo(p, p);
                    break;

                case STOP:
                    drawRect(p, p, SYM_SIZE, SYM_SIZE);
                    break;
                }
                endFill();
            }
            addChild(_symbol);
            addChild(_frame);

            addEventListener(MouseEvent.MOUSE_OUT, on_mouseout);
            addEventListener(MouseEvent.MOUSE_OVER, on_mouseover);
        }
    }
}
