(function(){var b=false;window.JQClass=function(){};JQClass.classes={};JQClass.extend=function a(c){var d=this.prototype;b=true;var e=new this();b=false;for(var i in c){e[i]=typeof c[i]=="function"&&typeof d[i]=="function"?(function(f,g){return function(){var h=this._super;this._super=function(k){return d[f].apply(this,k||[])};var l=g.apply(this,arguments);this._super=h;return l}})(i,c[i]):c[i]}function j(){if(!b&&this._init){this._init.apply(this,arguments)}}j.prototype=e;j.prototype.constructor=j;j.extend=a;return j}})();(function($){JQClass.classes.JQPlugin=JQClass.extend({name:"plugin",defaultOptions:{},regionalOptions:{},_getters:[],_getMarker:function(){return"is-"+this.name},_init:function(){$.extend(this.defaultOptions,(this.regionalOptions&&this.regionalOptions[""])||{});var c=camelCase(this.name);$[c]=this;$.fn[c]=function(a){var b=Array.prototype.slice.call(arguments,1);if($[c]._isNotChained(a,b)){return $[c][a].apply($[c],[this[0]].concat(b))}return this.each(function(){if(typeof a==="string"){if(a[0]==="_"||!$[c][a]){throw"Unknown method: "+a}$[c][a].apply($[c],[this].concat(b))}else{$[c]._attach(this,a)}})}},setDefaults:function(a){$.extend(this.defaultOptions,a||{})},_isNotChained:function(a,b){if(a==="option"&&(b.length===0||(b.length===1&&typeof b[0]==="string"))){return true}return $.inArray(a,this._getters)>-1},_attach:function(a,b){a=$(a);if(a.hasClass(this._getMarker())){return}a.addClass(this._getMarker());b=$.extend({},this.defaultOptions,this._getMetadata(a),b||{});var c=$.extend({name:this.name,elem:a,options:b},this._instSettings(a,b));a.data(this.name,c);this._postAttach(a,c);this.option(a,b)},_instSettings:function(a,b){return{}},_postAttach:function(a,b){},_getMetadata:function(d){try{var f=d.data(this.name.toLowerCase())||"";f=f.replace(/'/g,'"');f=f.replace(/([a-zA-Z0-9]+):/g,function(a,b,i){var c=f.substring(0,i).match(/"/g);return(!c||c.length%2===0?'"'+b+'":':b+":")});f=$.parseJSON("{"+f+"}");for(var g in f){var h=f[g];if(typeof h==="string"&&h.match(/^new Date\((.*)\)$/)){f[g]=eval(h)}}return f}catch(e){return{}}},_getInst:function(a){return $(a).data(this.name)||{}},option:function(a,b,c){a=$(a);var d=a.data(this.name);if(!b||(typeof b==="string"&&c==null)){var e=(d||{}).options;return(e&&b?e[b]:e)}if(!a.hasClass(this._getMarker())){return}var e=b||{};if(typeof b==="string"){e={};e[b]=c}this._optionsChanged(a,d,e);$.extend(d.options,e)},_optionsChanged:function(a,b,c){},destroy:function(a){a=$(a);if(!a.hasClass(this._getMarker())){return}this._preDestroy(a,this._getInst(a));a.removeData(this.name).removeClass(this._getMarker())},_preDestroy:function(a,b){}});function camelCase(c){return c.replace(/-([a-z])/g,function(a,b){return b.toUpperCase()})}$.JQPlugin={createPlugin:function(a,b){if(typeof a==="object"){b=a;a="JQPlugin"}a=camelCase(a);var c=camelCase(b.name);JQClass.classes[c]=JQClass.classes[a].extend(b);new JQClass.classes[c]()}}})(jQuery);(function(a){var g="countdown";var i=0;var e=1;var h=2;var b=3;var c=4;var d=5;var f=6;a.JQPlugin.createPlugin({name:g,defaultOptions:{until:null,since:null,timezone:null,serverSync:null,format:"dHMS",layout:"",compact:false,padZeroes:true,significant:0,description:"",expiryUrl:"",expiryText:"",alwaysExpire:false,onExpiry:null,onTick:null,tickInterval:1},regionalOptions:{"":{labels:["Years","Months","Weeks","Days","Hours","Minutes","Seconds"],labels1:["Year","Month","Week","Day","Hour","Minute","Second"],compactLabels:["y","m","w","d"],whichLabels:null,digits:["0","1","2","3","4","5","6","7","8","9"],timeSeparator:":",isRTL:false}},_getters:["getTimes"],_rtlClass:g+"-rtl",_sectionClass:g+"-section",_amountClass:g+"-amount",_periodClass:g+"-period",_rowClass:g+"-row",_holdingClass:g+"-holding",_showClass:g+"-show",_descrClass:g+"-descr",_timerElems:[],_init:function(){var j=this;this._super();this._serverSyncs=[];var k=(typeof Date.now=="function"?Date.now:function(){return new Date().getTime()});var l=(window.performance&&typeof window.performance.now=="function");function o(p){var q=(p<1000000000000?(l?(performance.now()+performance.timing.navigationStart):k()):p||k());if(q-n>=1000){j._updateElems();n=q}m(o)}var m=window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimationFrame||null;var n=0;if(!m||a.noRequestAnimationFrame){a.noRequestAnimationFrame=null;setInterval(function(){j._updateElems()},980)}else{n=window.animationStartTime||window.webkitAnimationStartTime||window.mozAnimationStartTime||window.oAnimationStartTime||window.msAnimationStartTime||k();m(o)}},UTCDate:function(j,k,l,n,o,p,q,r){if(typeof k=="object"&&k.constructor==Date){r=k.getMilliseconds();q=k.getSeconds();p=k.getMinutes();o=k.getHours();n=k.getDate();l=k.getMonth();k=k.getFullYear()}var m=new Date();m.setUTCFullYear(k);m.setUTCDate(1);m.setUTCMonth(l||0);m.setUTCDate(n||1);m.setUTCHours(o||0);m.setUTCMinutes((p||0)-(Math.abs(j)<30?j*60:j));m.setUTCSeconds(q||0);m.setUTCMilliseconds(r||0);return m},periodsToSeconds:function(j){return j[0]*31557600+j[1]*2629800+j[2]*604800+j[3]*86400+j[4]*3600+j[5]*60+j[6]},_instSettings:function(j,k){return{_periods:[0,0,0,0,0,0,0]}},_addElem:function(j){if(!this._hasElem(j)){this._timerElems.push(j)}},_hasElem:function(j){return(a.inArray(j,this._timerElems)>-1)},_removeElem:function(j){this._timerElems=a.map(this._timerElems,function(k){return(k==j?null:k)})},_updateElems:function(){for(var j=this._timerElems.length-1;j>=0;j--){this._updateCountdown(this._timerElems[j])}},_optionsChanged:function(j,k,l){if(l.layout){l.layout=l.layout.replace(/&lt;/g,"<").replace(/&gt;/g,">")}this._resetExtraLabels(k.options,l);var m=(k.options.timezone!=l.timezone);a.extend(k.options,l);this._adjustSettings(j,k,l.until!=null||l.since!=null||m);var n=new Date();if((k._since&&k._since<n)||(k._until&&k._until>n)){this._addElem(j[0])}this._updateCountdown(j,k)},_updateCountdown:function(j,k){j=j.jquery?j:a(j);k=k||this._getInst(j);if(!k){return}j.html(this._generateHTML(k)).toggleClass(this._rtlClass,k.options.isRTL);if(a.isFunction(k.options.onTick)){var l=k._hold!="lap"?k._periods:this._calculatePeriods(k,k._show,k.options.significant,new Date());if(k.options.tickInterval==1||this.periodsToSeconds(l)%k.options.tickInterval==0){k.options.onTick.apply(j[0],[l])}}var m=k._hold!="pause"&&(k._since?k._now.getTime()<k._since.getTime():k._now.getTime()>=k._until.getTime());if(m&&!k._expiring){k._expiring=true;if(this._hasElem(j[0])||k.options.alwaysExpire){this._removeElem(j[0]);if(a.isFunction(k.options.onExpiry)){k.options.onExpiry.apply(j[0],[])}if(k.options.expiryText){var n=k.options.layout;k.options.layout=k.options.expiryText;this._updateCountdown(j[0],k);k.options.layout=n}if(k.options.expiryUrl){window.location=k.options.expiryUrl}}k._expiring=false}else{if(k._hold=="pause"){this._removeElem(j[0])}}},_resetExtraLabels:function(j,k){for(var l in k){if(l.match(/[Ll]abels[02-9]|compactLabels1/)){j[l]=k[l]}}for(var l in j){if(l.match(/[Ll]abels[02-9]|compactLabels1/)&&typeof k[l]==="undefined"){j[l]=null}}},_adjustSettings:function(j,k,l){var m;var n=0;var o=null;for(var r=0;r<this._serverSyncs.length;r++){if(this._serverSyncs[r][0]==k.options.serverSync){o=this._serverSyncs[r][1];break}}if(o!=null){n=(k.options.serverSync?o:0);m=new Date()}else{var p=(a.isFunction(k.options.serverSync)?k.options.serverSync.apply(j[0],[]):null);m=new Date();n=(p?m.getTime()-p.getTime():0);this._serverSyncs.push([k.options.serverSync,n])}var q=k.options.timezone;q=(q==null?-m.getTimezoneOffset():q);if(l||(!l&&k._until==null&&k._since==null)){k._since=k.options.since;if(k._since!=null){k._since=this.UTCDate(q,this._determineTime(k._since,null));if(k._since&&n){k._since.setMilliseconds(k._since.getMilliseconds()+n)}}k._until=this.UTCDate(q,this._determineTime(k.options.until,m));if(n){k._until.setMilliseconds(k._until.getMilliseconds()+n)}}k._show=this._determineShow(k)},_preDestroy:function(j,k){this._removeElem(j[0]);j.empty()},pause:function(j){this._hold(j,"pause")},lap:function(j){this._hold(j,"lap")},resume:function(j){this._hold(j,null)},toggle:function(j){var k=a.data(j,this.name)||{};this[!k._hold?"pause":"resume"](j)},toggleLap:function(j){var k=a.data(j,this.name)||{};this[!k._hold?"lap":"resume"](j)},_hold:function(j,k){var l=a.data(j,this.name);if(l){if(l._hold=="pause"&&!k){l._periods=l._savePeriods;var m=(l._since?"-":"+");l[l._since?"_since":"_until"]=this._determineTime(m+l._periods[0]+"y"+m+l._periods[1]+"o"+m+l._periods[2]+"w"+m+l._periods[3]+"d"+m+l._periods[4]+"h"+m+l._periods[5]+"m"+m+l._periods[6]+"s");this._addElem(j)}l._hold=k;l._savePeriods=(k=="pause"?l._periods:null);a.data(j,this.name,l);this._updateCountdown(j,l)}},getTimes:function(j){var k=a.data(j,this.name);return(!k?null:(k._hold=="pause"?k._savePeriods:(!k._hold?k._periods:this._calculatePeriods(k,k._show,k.options.significant,new Date()))))},_determineTime:function(j,k){var l=this;var m=function(p){var q=new Date();q.setTime(q.getTime()+p*1000);return q};var n=function(F){F=F.toLowerCase();var p=new Date();var q=p.getFullYear();var r=p.getMonth();var v=p.getDate();var w=p.getHours();var x=p.getMinutes();var y=p.getSeconds();var D=/([+-]?[0-9]+)\s*(s|m|h|d|w|o|y)?/g;var E=D.exec(F);while(E){switch(E[2]||"s"){case"s":y+=parseInt(E[1],10);break;case"m":x+=parseInt(E[1],10);break;case"h":w+=parseInt(E[1],10);break;case"d":v+=parseInt(E[1],10);break;case"w":v+=parseInt(E[1],10)*7;break;case"o":r+=parseInt(E[1],10);v=Math.min(v,l._getDaysInMonth(q,r));break;case"y":q+=parseInt(E[1],10);v=Math.min(v,l._getDaysInMonth(q,r));break}E=D.exec(F)}return new Date(q,r,v,w,x,y,0)};var o=(j==null?k:(typeof j=="string"?n(j):(typeof j=="number"?m(j):j)));if(o){o.setMilliseconds(0)}return o},_getDaysInMonth:function(j,k){return 32-new Date(j,k,32).getDate()},_normalLabels:function(j){return j},_generateHTML:function(l){var n=this;l._periods=(l._hold?l._periods:this._calculatePeriods(l,l._show,l.options.significant,new Date()));var p=false;var r=0;var t=l.options.significant;var u=a.extend({},l._show);for(var v=i;v<=f;v++){p|=(l._show[v]=="?"&&l._periods[v]>0);u[v]=(l._show[v]=="?"&&!p?null:l._show[v]);r+=(u[v]?1:0);t-=(l._periods[v]>0?1:0)}var m=[false,false,false,false,false,false,false];for(var v=f;v>=i;v--){if(l._show[v]){if(l._periods[v]){m[v]=true}else{m[v]=t>0;t--}}}var o=(l.options.compact?l.options.compactLabels:l.options.labels);var q=l.options.whichLabels||this._normalLabels;var s=function(w){var x=l.options["compactLabels"+q(l._periods[w])];return(u[w]?n._translateDigits(l,l._periods[w])+(x?x[w]:o[w])+" ":"")};var j=(l.options.padZeroes?2:1);var k=function(w){var x=l.options["labels"+q(l._periods[w])];return((!l.options.significant&&u[w])||(l.options.significant&&m[w])?'<span class="'+n._sectionClass+'"><span class="'+n._amountClass+'">'+n._minDigits(l,l._periods[w],j)+'</span><span class="'+n._periodClass+'">'+(x?x[w]:o[w])+"</span></span>":"")};return(l.options.layout?this._buildLayout(l,u,l.options.layout,l.options.compact,l.options.significant,m):((l.options.compact?'<span class="'+this._rowClass+" "+this._amountClass+(l._hold?" "+this._holdingClass:"")+'">'+s(i)+s(e)+s(h)+s(b)+(u[c]?this._minDigits(l,l._periods[c],2):"")+(u[d]?(u[c]?l.options.timeSeparator:"")+this._minDigits(l,l._periods[d],2):"")+(u[f]?(u[c]||u[d]?l.options.timeSeparator:"")+this._minDigits(l,l._periods[f],2):""):'<span class="'+this._rowClass+" "+this._showClass+(l.options.significant||r)+(l._hold?" "+this._holdingClass:"")+'">'+k(i)+k(e)+k(h)+k(b)+k(c)+k(d)+k(f))+"</span>"+(l.options.description?'<span class="'+this._rowClass+" "+this._descrClass+'">'+l.options.description+"</span>":"")))},_buildLayout:function(t,v,x,u,w,k){var o=t.options[u?"compactLabels":"labels"];var q=t.options.whichLabels||this._normalLabels;var j=function(y){return(t.options[(u?"compactLabels":"labels")+q(t._periods[y])]||o)[y]};var l=function(y,z){return t.options.digits[Math.floor(y/z)%10]};var n={desc:t.options.description,sep:t.options.timeSeparator,yl:j(i),yn:this._minDigits(t,t._periods[i],1),ynn:this._minDigits(t,t._periods[i],2),ynnn:this._minDigits(t,t._periods[i],3),y1:l(t._periods[i],1),y10:l(t._periods[i],10),y100:l(t._periods[i],100),y1000:l(t._periods[i],1000),ol:j(e),on:this._minDigits(t,t._periods[e],1),onn:this._minDigits(t,t._periods[e],2),onnn:this._minDigits(t,t._periods[e],3),o1:l(t._periods[e],1),o10:l(t._periods[e],10),o100:l(t._periods[e],100),o1000:l(t._periods[e],1000),wl:j(h),wn:this._minDigits(t,t._periods[h],1),wnn:this._minDigits(t,t._periods[h],2),wnnn:this._minDigits(t,t._periods[h],3),w1:l(t._periods[h],1),w10:l(t._periods[h],10),w100:l(t._periods[h],100),w1000:l(t._periods[h],1000),dl:j(b),dn:this._minDigits(t,t._periods[b],1),dnn:this._minDigits(t,t._periods[b],2),dnnn:this._minDigits(t,t._periods[b],3),d1:l(t._periods[b],1),d10:l(t._periods[b],10),d100:l(t._periods[b],100),d1000:l(t._periods[b],1000),hl:j(c),hn:this._minDigits(t,t._periods[c],1),hnn:this._minDigits(t,t._periods[c],2),hnnn:this._minDigits(t,t._periods[c],3),h1:l(t._periods[c],1),h10:l(t._periods[c],10),h100:l(t._periods[c],100),h1000:l(t._periods[c],1000),ml:j(d),mn:this._minDigits(t,t._periods[d],1),mnn:this._minDigits(t,t._periods[d],2),mnnn:this._minDigits(t,t._periods[d],3),m1:l(t._periods[d],1),m10:l(t._periods[d],10),m100:l(t._periods[d],100),m1000:l(t._periods[d],1000),sl:j(f),sn:this._minDigits(t,t._periods[f],1),snn:this._minDigits(t,t._periods[f],2),snnn:this._minDigits(t,t._periods[f],3),s1:l(t._periods[f],1),s10:l(t._periods[f],10),s100:l(t._periods[f],100),s1000:l(t._periods[f],1000)};var p=x;for(var m=i;m<=f;m++){var r="yowdhms".charAt(m);var s=new RegExp("\\{"+r+"<\\}([\\s\\S]*)\\{"+r+">\\}","g");p=p.replace(s,((!w&&v[m])||(w&&k[m])?"$1":""))}a.each(n,function(A,y){var z=new RegExp("\\{"+A+"\\}","g");p=p.replace(z,y)});return p},_minDigits:function(j,k,l){k=""+k;if(k.length>=l){return this._translateDigits(j,k)}k="0000000000"+k;return this._translateDigits(j,k.substr(k.length-l))},_translateDigits:function(j,k){return(""+k).replace(/[0-9]/g,function(l){return j.options.digits[l]})},_determineShow:function(j){var k=j.options.format;var l=[];l[i]=(k.match("y")?"?":(k.match("Y")?"!":null));l[e]=(k.match("o")?"?":(k.match("O")?"!":null));l[h]=(k.match("w")?"?":(k.match("W")?"!":null));l[b]=(k.match("d")?"?":(k.match("D")?"!":null));l[c]=(k.match("h")?"?":(k.match("H")?"!":null));l[d]=(k.match("m")?"?":(k.match("M")?"!":null));l[f]=(k.match("s")?"?":(k.match("S")?"!":null));return l},_calculatePeriods:function(z,A,j,l){z._now=l;z._now.setMilliseconds(0);var n=new Date(z._now.getTime());if(z._since){if(l.getTime()<z._since.getTime()){z._now=l=n}else{l=z._since}}else{n.setTime(z._until.getTime());if(l.getTime()>z._until.getTime()){z._now=l=n}}var o=[0,0,0,0,0,0,0];if(A[i]||A[e]){var q=this._getDaysInMonth(l.getFullYear(),l.getMonth());var v=this._getDaysInMonth(n.getFullYear(),n.getMonth());var x=(n.getDate()==l.getDate()||(n.getDate()>=Math.min(q,v)&&l.getDate()>=Math.min(q,v)));var C=function(s){return(s.getHours()*60+s.getMinutes())*60+s.getSeconds()};var D=Math.max(0,(n.getFullYear()-l.getFullYear())*12+n.getMonth()-l.getMonth()+((n.getDate()<l.getDate()&&!x)||(x&&C(n)<C(l))?-1:0));o[i]=(A[i]?Math.floor(D/12):0);o[e]=(A[e]?D-o[i]*12:0);l=new Date(l.getTime());var E=(l.getDate()==q);var p=this._getDaysInMonth(l.getFullYear()+o[i],l.getMonth()+o[e]);if(l.getDate()>p){l.setDate(p)}l.setFullYear(l.getFullYear()+o[i]);l.setMonth(l.getMonth()+o[e]);if(E){l.setDate(p)}}var r=Math.floor((n.getTime()-l.getTime())/1000);var B=function(s,t){o[s]=(A[s]?Math.floor(r/t):0);r-=o[s]*t};B(h,604800);B(b,86400);B(c,3600);B(d,60);B(f,1);if(r>0&&!z._since){var k=[1,12,4.3482,7,24,60,60];var m=f;var w=1;for(var y=f;y>=i;y--){if(A[y]){if(o[m]>=w){o[m]=0;r=1}if(r>0){o[y]++;r=0;m=y;w=1}}w*=k[y]}}if(j){for(var y=i;y<=f;y++){if(j&&o[y]){j--}else{if(!j){o[y]=0}}}}return o}})})(jQuery);