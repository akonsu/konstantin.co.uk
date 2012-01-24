// -*-java-*- Time-stamp: <baraban.js - root>
// copyright (c) konstantin.co.uk. all rights reserved.

var Baraban = Class.create({
    initialize : function(options)
    {
        var container = options['container'];
        var vertical = options['vertical'];

        this.size = options['size'];
        this.url = options['url'];

        var a_next = new Element('a', {href : '#', style : 'white-space:nowrap;'}).update('+');
        var a_prev = new Element('a', {href : '#', style : 'white-space:nowrap;'}).update('-');
        var tbody = new Element('tbody');
        var td_next = new Element('td', {style : 'background-color:lightgrey;padding:5px;text-align:center;white-space:nowrap;'}).insert('[').insert(a_next).insert(']');
        var td_prev = new Element('td', {style : 'background-color:lightgrey;padding:5px;text-align:center;white-space:nowrap;'}).insert('[').insert(a_prev).insert(']');

        this.list = new Element('td', {style : 'white-space:nowrap;'});

        if (vertical)
        {
            this.button_next = new Element('tr').insert(td_next);
            this.button_prev = new Element('tr').insert(td_prev);
            this.item_display = 'block';

            tbody.insert(this.button_prev).insert(new Element('tr').insert(this.list)).insert(this.button_next);
        }
        else
        {
            this.button_next = td_next;
            this.button_prev = td_prev;
            this.item_display = 'inline-block';

            tbody.insert(new Element('tr').insert(this.button_prev).insert(this.list).insert(this.button_next));
        }
        if (container)
        {
            container.update(new Element('table', {cellpadding : 0, cellspacing : 5}).update(tbody));
        }

        this.cursor = 0;
        this.items = []
        this.limit = 0;
        this.offset = 0;

        new Ajax.Request(this.url, {
          method : 'get',
          parameters : {count : this.size * 2, offset : this.offset},
          onSuccess : this.push_items.bind(this)
        });

        a_next.observe('click', this.on_next.bindAsEventListener(this));
        a_prev.observe('click', this.on_prev.bindAsEventListener(this));
    },

    mk_item : function(h)
    {
        return new Element('a', h['link']).insert(new Element('img', h['thumbnail']));
    },

    on_next : function(event)
    {
        var length = this.items.length;

        if (this.cursor + this.size < length)
        {
            this.cursor++;
            this.update(true);

            if (this.cursor + this.size >= length && (this.limit <= 0 || length < this.limit - this.offset))
            {
                new Ajax.Request(this.url, {
                    method : 'get',
                    parameters : {count : this.size, offset : this.offset + length},
                    onSuccess : this.push_items.bind(this)
                    });
            }
        }
    },

    on_prev : function(event)
    {
        if (this.cursor > 0)
        {
            this.cursor--;
            this.update(true);

            if (this.cursor <= 0 && this.offset > 0)
            {
                new Ajax.Request(this.url, {
                    method : 'get',
                    parameters : {count : Math.min(this.offset, this.size), offset : Math.max(0, this.offset - this.size)},
                    onSuccess : this.unshift_items.bind(this)
                    });
            }
        }
    },

    push_items : function(transport)
    {
        var data = transport.responseJSON;

        if (Object.isArray(data))
        {
            var parameters = transport.request.parameters;
            var count = parameters['count'];
            var length = data.length;

            if (this.limit <= 0 && length < count)
            {
                this.limit = parameters['offset'] + length;
            }
            if (length > 0)
            {
                var k = this.cursor - this.size;

                if (k > 0)
                {
                    this.items.splice(0, k);

                    this.cursor = this.size;
                    this.offset += k;
                }
                this.items = this.items.concat(data);
                this.update(this.cursor + this.size > this.items.length - length);
            }
        }
    },

    unshift_items : function(transport)
    {
        var data = transport.responseJSON;

        if (Object.isArray(data))
        {
            var length = data.length;

            if (length > 0)
            {
                var k = this.items.length - this.cursor - this.size * 2;

                if (k > 0)
                {
                    this.items.splice(-k, k);
                }
                this.cursor += length;
                this.offset -= length;

                this.items = data.concat(this.items);
                this.update(false);
            }
        }
    },

    update : function(b)
    {
        if (b)
        {
            var length = Math.min(this.items.length, this.cursor + this.size);

            this.list.update();

            for (var i = this.cursor; i < length; i++)
            {
                this.list.insert(this.mk_item(this.items[i]).setStyle({display : this.item_display}));
            }
        }
        if (this.cursor + this.size < this.items.length)
        {
            this.button_next.show();
        }
        else
        {
            this.button_next.hide();
        }
        if (this.cursor > 0)
        {
            this.button_prev.show();
        }
        else
        {
            this.button_prev.hide();
        }
    }
});
