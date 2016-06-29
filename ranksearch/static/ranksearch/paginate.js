/*global $, _, Backbone */

var Sitter = Backbone.Model.extend({});

var Sitters = Backbone.Collection.extend({
    comparator: function(a) { return -1 * a.get('score'); }
});


var SittersView = Backbone.View.extend({
    initialize: function(options) {
        options = options || {};
        this.parent_collection = options.collection || new Sitters([]);
        if (!options.el) {
            this.setElement($('#sitters'));
        }
        this.currentPage = options.page || 0;
        this.minScore = 0;
        this.interval = 10;
        this.readFromTable();
    },

    readFromTable: function() {
        var unpackRow = function(index, row) {
            return {
                'name': $('td:nth-child(2) a', row).text(),
                'link': $('td:nth-child(2) a', row).attr('href'),
                'image': $('td:nth-child(1) img', row).attr('src'),
                'score': parseFloat($('td:nth-child(3)', row).text())
            };
        };
        var data = this.$('table tr').map(unpackRow);
        this.parent_collection.reset(data.get());
        this.runFilter();
        return this;
    },

    runFilter: function() {
        this.collection = new Sitters(this.parent_collection.filter(function(i) {
            return i.get('score') >= this.minScore; }.bind(this)));
        return this;
    },
    
    events: {
        'click .next': 'next',
        'click .prev': 'prev',
        'click .page': 'page',
        'change #range': 'range',
        'input #range': 'range'
    },

    turn: function(page) {
        if ((page < 0) || ((page * this.interval) > this.collection.length)) { 
            page = 0;
        }
        this.currentPage = page;
        this.render();
        var oldsearch = window.location.search;
        var newsearch = window.location.search.replace(
                /(((\?|\&)page=\d+)|$)/,
            function() { return (arguments[3] || '?') + 'page=' + (parseInt(page, 10) + 1); });
        window.history.pushState({page: page}, "", newsearch);
        return this;
    },

    range: function(event) {
        var handler = function() {
            this.minScore = parseFloat(event.target.value);
            this.$('#minscore').text(this.minScore);
            return this.runFilter().renderPaginator().renderTable();
        }.bind(this);
        _.debounce(handler, 200)();
    },

    page: function(e) { return this.turn(parseInt($(e.target).text(), 10) - 1); },
    next: function(e) { return this.page(this.currentPage + 1); },
    prev: function(e) { return this.page(this.currentPage - 1); },

    context: function() {
        return {
            minScore: this.minScore,
            start: this.currentPage * this.interval,
            interval: this.interval,
            all: this.collection.length,
            sitters: this.collection.toJSON()
        };
    },
    
    renderRange: function() {
        this.$('#range').html(this._rangeTemplate(this.context()));
        this.$('#range').fadeIn(150);
        return this;
    },

    renderPaginator: function() {
        this.$('#paginator').html(this._pagerTemplate(this.context()));
        this.$('#paginator ul').fadeIn(150);
        return this;
    },

    renderTable: function() {
        this.$('#sittertable').html(this._tableTemplate(this.context()));
        this.$('#sittertable').fadeIn(150);
        return this;
    },
    
    render: function() {
        var promises = _.map('#sittertable', '#paginator ul', '#range', function(sel) {
            return this.$(sel).fadeOut(150);
        }.bind(this));

        $.when(promises).then(function() {
            this.renderRange();
            this.renderPaginator();
            this.renderTable();
        }.bind(this));
        return this;
    },

    _rangeTemplate: _.template([
        '<input type="range" max="5" min="0" ',
        'step="0.25" value="<%= minScore %>"> ',
        'Now showing scores above: <span id="minscore"><%= minScore %></span>'].join('')),

    _pagerTemplate: _.template([
        'Page: <ul>',
        '<% for(var i=0,l=interval; i < all; i += l) { var p = Math.floor(i / l) + 1; %> ',
        '  <li><a class="page"><%= p %></a></li>',
        '<% } %>',
        '</ul>'].join('\n')),
    
    _tableTemplate: _.template([
        '<% for(var i=start, l=interval; (i < start + interval) && (i < all); i += 1) { var s = sitters[i]; %>',
        '  <tr>',
        '    <td><img src="<%= s.image %>"></td>',
        '    <td><a href="<%= s.link %>"><%= s.name %></a></td>',
        '    <td><%= s.score %></td>',
        '  </tr>',
        '<% } %>'
    ].join('\n'))
});
        
    
$(function() {
    var pageset = (window.location.search.match(/((\?|\&)page=(\d+))/));
    var page = (pageset && pageset[3]) ? (parseInt(pageset[3], 10) - 1) : 0;
    var sitters = new SittersView({page: page}).render();
});
