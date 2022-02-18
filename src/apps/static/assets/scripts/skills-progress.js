(function(){var b=[].indexOf||function(f){for(var c=0,d=this.length;c<d;c++){if(c in this&&this[c]===f){return c}}return -1},a=[].slice;(function(d,c){if(typeof define==="function"&&define.amd){return define("waypoints",["jquery"],function(e){return c(e,d)})}else{return c(d.jQuery,d)}})(this,function(x,H){var I,E,e,t,B,c,F,j,D,z,G,A,d,q,C,k;I=x(H);j=b.call(H,"ontouchstart")>=0;t={horizontal:{},vertical:{}};B=1;F={};c="waypoints-context-id";G="resize.waypoints";A="scroll.waypoints";d=1;q="waypoints-waypoint-ids";C="waypoint";k="waypoints";E=function(){function f(h){var g=this;this.$element=h;this.element=h[0];this.didResize=false;this.didScroll=false;this.id="context"+B++;this.oldScroll={x:h.scrollLeft(),y:h.scrollTop()};this.waypoints={horizontal:{},vertical:{}};h.data(c,this.id);F[this.id]=this;h.bind(A,function(){var i;if(!(g.didScroll||j)){g.didScroll=true;i=function(){g.doScroll();return g.didScroll=false};return H.setTimeout(i,x[k].settings.scrollThrottle)}});h.bind(G,function(){var i;if(!g.didResize){g.didResize=true;i=function(){x[k]("refresh");return g.didResize=false};return H.setTimeout(i,x[k].settings.resizeThrottle)}})}f.prototype.doScroll=function(){var h,g=this;h={horizontal:{newScroll:this.$element.scrollLeft(),oldScroll:this.oldScroll.x,forward:"right",backward:"left"},vertical:{newScroll:this.$element.scrollTop(),oldScroll:this.oldScroll.y,forward:"down",backward:"up"}};if(j&&(!h.vertical.oldScroll||!h.vertical.newScroll)){x[k]("refresh")}x.each(h,function(l,i){var m,o,n;n=[];o=i.newScroll>i.oldScroll;m=o?i.forward:i.backward;x.each(g.waypoints[l],function(u,p){var s,r;if(i.oldScroll<(s=p.offset)&&s<=i.newScroll){return n.push(p)}else{if(i.newScroll<(r=p.offset)&&r<=i.oldScroll){return n.push(p)}}});n.sort(function(r,p){return r.offset-p.offset});if(!o){n.reverse()}return x.each(n,function(r,p){if(p.options.continuous||r===n.length-1){return p.trigger([m])}})});return this.oldScroll={x:h.horizontal.newScroll,y:h.vertical.newScroll}};f.prototype.refresh=function(){var l,g,i,h=this;i=x.isWindow(this.element);g=this.$element.offset();this.doScroll();l={horizontal:{contextOffset:i?0:g.left,contextScroll:i?0:this.oldScroll.x,contextDimension:this.$element.width(),oldScroll:this.oldScroll.x,forward:"right",backward:"left",offsetProp:"left"},vertical:{contextOffset:i?0:g.top,contextScroll:i?0:this.oldScroll.y,contextDimension:i?x[k]("viewportHeight"):this.$element.height(),oldScroll:this.oldScroll.y,forward:"down",backward:"up",offsetProp:"top"}};return x.each(l,function(n,m){return x.each(h.waypoints[n],function(w,u){var p,s,r,v,o;p=u.options.offset;r=u.offset;s=x.isWindow(u.element)?0:u.$element.offset()[m.offsetProp];if(x.isFunction(p)){p=p.apply(u.element)}else{if(typeof p==="string"){p=parseFloat(p);if(u.options.offset.indexOf("%")>-1){p=Math.ceil(m.contextDimension*p/100)}}}u.offset=s-m.contextOffset+m.contextScroll-p;if(u.options.onlyOnScroll&&r!=null||!u.enabled){return}if(r!==null&&r<(v=m.oldScroll)&&v<=u.offset){return u.trigger([m.backward])}else{if(r!==null&&r>(o=m.oldScroll)&&o>=u.offset){return u.trigger([m.forward])}else{if(r===null&&m.oldScroll>=u.offset){return u.trigger([m.forward])}}}})})};f.prototype.checkEmpty=function(){if(x.isEmptyObject(this.waypoints.horizontal)&&x.isEmptyObject(this.waypoints.vertical)){this.$element.unbind([G,A].join(" "));return delete F[this.id]}};return f}();e=function(){function f(m,g,l){var h,i;l=x.extend({},x.fn[C].defaults,l);if(l.offset==="bottom-in-view"){l.offset=function(){var n;n=x[k]("viewportHeight");if(!x.isWindow(g.element)){n=g.$element.height()}return n-x(this).outerHeight()}}this.$element=m;this.element=m[0];this.axis=l.horizontal?"horizontal":"vertical";this.callback=l.handler;this.context=g;this.enabled=l.enabled;this.id="waypoints"+d++;this.offset=null;this.options=l;g.waypoints[this.axis][this.id]=this;t[this.axis][this.id]=this;h=(i=m.data(q))!=null?i:[];h.push(this.id);m.data(q,h)}f.prototype.trigger=function(g){if(!this.enabled){return}if(this.callback!=null){this.callback.apply(this.element,g)}if(this.options.triggerOnce){return this.destroy()}};f.prototype.disable=function(){return this.enabled=false};f.prototype.enable=function(){this.context.refresh();return this.enabled=true};f.prototype.destroy=function(){delete t[this.axis][this.id];delete this.context.waypoints[this.axis][this.id];return this.context.checkEmpty()};f.getWaypointsByElement=function(i){var g,h;h=x(i).data(q);if(!h){return[]}g=x.extend({},t.horizontal,t.vertical);return x.map(h,function(l){return g[l]})};return f}();z={init:function(h,f){var g;if(f==null){f={}}if((g=f.handler)==null){f.handler=h}this.each(function(){var n,l,i,m;n=x(this);i=(m=f.context)!=null?m:x.fn[C].defaults.context;if(!x.isWindow(i)){i=n.closest(i)}i=x(i);l=F[i.data(c)];if(!l){l=new E(i)}return new e(n,l,f)});x[k]("refresh");return this},disable:function(){return z._invoke(this,"disable")},enable:function(){return z._invoke(this,"enable")},destroy:function(){return z._invoke(this,"destroy")},prev:function(g,f){return z._traverse.call(this,g,f,function(l,h,i){if(h>0){return l.push(i[h-1])}})},next:function(g,f){return z._traverse.call(this,g,f,function(l,h,i){if(h<i.length-1){return l.push(i[h+1])}})},_traverse:function(l,f,g){var i,h;if(l==null){l="vertical"}if(f==null){f=H}h=D.aggregate(f);i=[];this.each(function(){var m;m=x.inArray(this,h[l]);return g(i,m,h[l])});return this.pushStack(i)},_invoke:function(g,f){g.each(function(){var h;h=e.getWaypointsByElement(this);return x.each(h,function(l,i){i[f]();return true})});return this}};x.fn[C]=function(){var g,f;f=arguments[0],g=2<=arguments.length?a.call(arguments,1):[];if(z[f]){return z[f].apply(this,g)}else{if(x.isFunction(f)){return z.init.apply(this,arguments)}else{if(x.isPlainObject(f)){return z.init.apply(this,[null,f])}else{if(!f){return x.error("jQuery Waypoints needs a callback function or handler option.")}else{return x.error("The "+f+" method does not exist in jQuery Waypoints.")}}}}};x.fn[C].defaults={context:H,continuous:true,enabled:true,horizontal:false,offset:0,triggerOnce:false};D={refresh:function(){return x.each(F,function(g,f){return f.refresh()})},viewportHeight:function(){var f;return(f=H.innerHeight)!=null?f:I.height()},aggregate:function(i){var f,h,g;f=t;if(i){f=(g=F[x(i).data(c)])!=null?g.waypoints:void 0}if(!f){return[]}h={horizontal:[],vertical:[]};x.each(h,function(m,l){x.each(f[m],function(o,n){return l.push(n)});l.sort(function(o,n){return o.offset-n.offset});h[m]=x.map(l,function(n){return n.element});return h[m]=x.unique(h[m])});return h},above:function(f){if(f==null){f=H}return D._filter(f,"vertical",function(h,g){return g.offset<=h.oldScroll.y})},below:function(f){if(f==null){f=H}return D._filter(f,"vertical",function(h,g){return g.offset>h.oldScroll.y})},left:function(f){if(f==null){f=H}return D._filter(f,"horizontal",function(h,g){return g.offset<=h.oldScroll.x})},right:function(f){if(f==null){f=H}return D._filter(f,"horizontal",function(h,g){return g.offset>h.oldScroll.x})},enable:function(){return D._invoke("enable")},disable:function(){return D._invoke("disable")},destroy:function(){return D._invoke("destroy")},extendFn:function(g,f){return z[g]=f},_invoke:function(g){var f;f=x.extend({},t.vertical,t.horizontal);return x.each(f,function(h,i){i[g]();return true})},_filter:function(l,f,i){var g,h;g=F[x(l).data(c)];if(!g){return[]}h=[];x.each(g.waypoints[f],function(n,m){if(i(g,m)){return h.push(m)}});h.sort(function(n,m){return n.offset-m.offset});return x.map(h,function(m){return m.element})}};x[k]=function(){var g,f;f=arguments[0],g=2<=arguments.length?a.call(arguments,1):[];if(D[f]){return D[f].apply(null,g)}else{return D.aggregate.call(null,f)}};x[k].settings={resizeThrottle:100,scrollThrottle:30};return I.load(function(){return x[k]("refresh")})})}).call(this);
