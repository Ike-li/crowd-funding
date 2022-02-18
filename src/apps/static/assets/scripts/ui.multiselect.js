(function(a){a.widget("ui.multiselect",{options:{sortable:true,searchable:true,doubleClickable:true,animated:"fast",show:"slideDown",hide:"slideUp",dividerLocation:0.6,availableFirst:false,nodeComparator:function(b,c){var d=b.text(),e=c.text();return d==e?0:(d<e?-1:1)}},_create:function(){this.element.hide();this.id=this.element.attr("id");this.container=a('<div class="ui-multiselect ui-helper-clearfix ui-widget"></div>').insertAfter(this.element);this.count=0;this.selectedContainer=a("").appendTo(this.container);this.availableContainer=a('<div class="available"></div>')[this.options.availableFirst?"prependTo":"appendTo"](this.container);this.selectedActions=a('<div class="actions ui-widget-header ui-helper-clearfix"><span class="count">0 '+a.ui.multiselect.locale.itemsCount+'</span><a href="#" class="remove-all">'+a.ui.multiselect.locale.removeAll+"</a></div>").appendTo(this.selectedContainer);this.availableActions=a('<div class="actions ui-widget-header ui-helper-clearfix"><strong>Categories</strong><a href="#" class="add-all">'+a.ui.multiselect.locale.addAll+"</a></div>").appendTo(this.availableContainer);this.selectedList=a('<ul class="selected connected-list"></ul>').bind("selectstart",function(){return false}).appendTo(this.selectedContainer);this.availableList=a('<ul class="available connected-list"></ul>').bind("selectstart",function(){return false}).appendTo(this.availableContainer);var b=this;this.container.width(this.element.width()+1);this.selectedContainer.width(Math.floor(this.element.width()*this.options.dividerLocation));this.availableContainer.width(Math.floor(this.element.width()*(1-this.options.dividerLocation)));this.selectedList.height(Math.max(this.element.height()-this.selectedActions.height(),1));this.availableList.height(Math.max(this.element.height()-this.availableActions.height(),1));if(!this.options.animated){this.options.show="show";this.options.hide="hide"}this._populateLists(this.element.find("option"));if(this.options.sortable){this.selectedList.sortable({placeholder:"ui-state-highlight",axis:"y",update:function(c,d){b.selectedList.find("li").each(function(){if(a(this).data("optionLink")){a(this).data("optionLink").remove().appendTo(b.element)}})},receive:function(c,d){d.item.data("optionLink").attr("selected",true);b.count+=1;b._updateCount();b.selectedList.children(".ui-draggable").each(function(){a(this).removeClass("ui-draggable");a(this).data("optionLink",d.item.data("optionLink"));a(this).data("idx",d.item.data("idx"));b._applyItemState(a(this),true)});setTimeout(function(){d.item.remove()},1)}})}if(this.options.searchable){this._registerSearchEvents(this.availableContainer.find("input.search"))}else{a(".search").hide()}this.container.find(".remove-all").click(function(){b._populateLists(b.element.find("option").removeAttr("selected"));return false});this.container.find(".add-all").click(function(){var c=b.element.find("option").not(":selected");if(b.availableList.children("li:hidden").length>1){b.availableList.children("li").each(function(d){if(a(this).is(":visible")){a(c[d-1]).attr("selected","selected")}})}else{c.attr("selected","selected")}b._populateLists(b.element.find("option"));return false})},destroy:function(){this.element.show();this.container.remove();a.Widget.prototype.destroy.apply(this,arguments)},_populateLists:function(c){this.selectedList.children(".ui-element").remove();this.availableList.children(".ui-element").remove();this.count=0;var d=this;var b=a(c.map(function(e){var f=d._getOptionNode(this).appendTo(this.selected?d.selectedList:d.availableList).show();if(this.selected){d.count+=1}d._applyItemState(f,this.selected);f.data("idx",e);return f[0]}))},_updateCount:function(){this.element.trigger("change");this.selectedContainer.find("span.count").text(this.count+" "+a.ui.multiselect.locale.itemsCount)},_getOptionNode:function(c){c=a(c);var b=a('<li class="ui-state-default ui-element" title="'+c.text()+'"><span class="ui-icon"/>'+c.text()+'<a href="#" class="action"><span class="ui-corner-all ui-icon"/></a></li>').hide();b.data("optionLink",c);return b},_cloneWithData:function(c){var b=c.clone(false,false);b.data("optionLink",c.data("optionLink"));b.data("idx",c.data("idx"));return b},_setSelected:function(f,h){f.data("optionLink").attr("selected",h);if(h){var j=this._cloneWithData(f);f[this.options.hide](this.options.animated,function(){a(this).remove()});j.appendTo(this.selectedList).hide()[this.options.show](this.options.animated);this._applyItemState(j,true);return j}else{var g=this.availableList.find("li"),c=this.options.nodeComparator;var k=null,e=f.data("idx"),d=c(f,a(g[e]));if(d){while(e>=0&&e<g.length){d>0?e++:e--;if(d!=c(f,a(g[e]))){k=g[d>0?e:e+1];break}}}else{k=g[e]}var b=this._cloneWithData(f);k?b.insertBefore(a(k)):b.appendTo(this.availableList);f[this.options.hide](this.options.animated,function(){a(this).remove()});b.hide()[this.options.show](this.options.animated);this._applyItemState(b,false);return b}},_applyItemState:function(b,c){if(c){if(this.options.sortable){b.children("span").addClass("ui-icon-arrowthick-2-n-s").removeClass("ui-helper-hidden").addClass("ui-icon")}else{b.children("span").removeClass("ui-icon-arrowthick-2-n-s").addClass("ui-helper-hidden").removeClass("ui-icon")}b.find("a.action span").addClass("ui-icon-minus").removeClass("ui-icon-plus");this._registerRemoveEvents(b.find("a.action"))}else{b.children("span").removeClass("ui-icon-arrowthick-2-n-s").addClass("ui-helper-hidden").removeClass("ui-icon");b.find("a.action span").addClass("ui-icon-plus").removeClass("ui-icon-minus");this._registerAddEvents(b.find("a.action"))}this._registerDoubleClickEvents(b);this._registerHoverEvents(b)},_registerDoubleClickEvents:function(b){if(!this.options.doubleClickable){return}b.dblclick(function(c){if(a(c.target).closest(".action").length===0){b.find("a.action").click()}})},_registerHoverEvents:function(b){b.removeClass("ui-state-hover");b.mouseover(function(){a(this).addClass("ui-state-hover")});b.mouseout(function(){a(this).removeClass("ui-state-hover")})},_registerAddEvents:function(b){var c=this;b.click(function(){var d=c._setSelected(a(this).parent(),true);c.count+=1;c._updateCount();return false});if(this.options.sortable){b.each(function(){a(this).parent().draggable({connectToSortable:c.selectedList,helper:function(){var d=c._cloneWithData(a(this)).width(a(this).width()-50);d.width(a(this).width());return d},appendTo:c.container,containment:c.container,revert:"invalid"})})}},_registerRemoveEvents:function(b){var c=this;b.click(function(){c._setSelected(a(this).parent(),false);c.count-=1;c._updateCount();return false})},_registerSearchEvents:function(b){var c=this;b.focus(function(){a(this).addClass("ui-state-active")}).blur(function(){a(this).removeClass("ui-state-active")}).keypress(function(d){if(d.keyCode==13){return false}}).keyup(function(){c._filter.apply(this,[c.availableList])})}});a.extend(a.ui.multiselect,{locale:{addAll:"3 Item Selected",removeAll:"Remove all",itemsCount:"items selected"}})})(jQuery);
