window.Modernizr=function(av,ay,T){function af(a){Z.cssText=a}function O(a,b){return af(ac.join(a+";")+(b||""))}function W(a,b){return typeof a===b}function ae(a,b){return !!~(""+a).indexOf(b)}function N(a,b){for(var c in a){var d=a[c];if(!ae(d,"-")&&Z[d]!==T){return b=="pfx"?d:!0}}return !1}function V(a,b,c){for(var d in a){var e=b[a[d]];if(e!==T){return c===!1?a[d]:W(e,"function")?e.bind(c||b):e}}return !1}function ad(a,b,c){var d=a.charAt(0).toUpperCase()+a.slice(1),e=(a+" "+ai.join(d+" ")+d).split(" ");return W(b,"string")||W(b,"undefined")?N(e,b):(e=(a+" "+ak.join(d+" ")+d).split(" "),V(e,b,c))}function M(){aj.input=function(a){for(var b=0,c=a.length;b<c;b++){ao[a[b]]=a[b] in ah}return ao.list&&(ao.list=!!ay.createElement("datalist")&&!!av.HTMLDataListElement),ao}("autocomplete autofocus list placeholder max min multiple pattern required step".split(" ")),aj.inputtypes=function(a){for(var b=0,c,d,e,f=a.length;b<f;b++){ah.setAttribute("type",d=a[b]),c=ah.type!=="text",c&&(ah.value=Q,ah.style.cssText="position:absolute;visibility:hidden;",/^range$/.test(d)&&ah.style.WebkitAppearance!==T?(aa.appendChild(ah),e=ay.defaultView,c=e.getComputedStyle&&e.getComputedStyle(ah,null).WebkitAppearance!=="textfield"&&ah.offsetHeight!==0,aa.removeChild(ah)):/^(search|tel)$/.test(d)||(/^(url|email)$/.test(d)?c=ah.checkValidity&&ah.checkValidity()===!1:c=ah.value!=Q)),an[a[b]]=!!c}return an}("search tel url email datetime date month week time datetime-local number range color".split(" "))}var ab="2.8.3",aj={},S=!0,aa=ay.documentElement,ax="modernizr",R=ay.createElement(ax),Z=R.style,ah=ay.createElement("input"),Q=":)",Y={}.toString,ac=" -webkit- -moz- -o- -ms- ".split(" "),ag="Webkit Moz O ms",ai=ag.split(" "),ak=ag.toLowerCase().split(" "),al={svg:"http://www.w3.org/2000/svg"},am={},an={},ao={},ap=[],aq=ap.slice,ar,at=function(a,b,c,d){var e,f,g,h,i=ay.createElement("div"),j=ay.body,k=j||ay.createElement("body");if(parseInt(c,10)){while(c--){g=ay.createElement("div"),g.id=d?d[c]:ax+(c+1),i.appendChild(g)}}return e=["&#173;",'<style id="s',ax,'">',a,"</style>"].join(""),i.id=ax,(j?i:k).innerHTML+=e,k.appendChild(i),j||(k.style.background="",k.style.overflow="hidden",h=aa.style.overflow,aa.style.overflow="hidden",aa.appendChild(k)),f=b(i,a),j?i.parentNode.removeChild(i):(k.parentNode.removeChild(k),aa.style.overflow=h),!!f},au=function(a){var b=av.matchMedia||av.msMatchMedia;if(b){return b(a)&&b(a).matches||!1}var c;return at("@media "+a+" { #"+ax+" { position: absolute; } }",function(d){c=(av.getComputedStyle?getComputedStyle(d,null):d.currentStyle)["position"]=="absolute"}),c},aw=function(){function b(c,d){d=d||ay.createElement(a[c]||"div"),c="on"+c;var e=c in d;return e||(d.setAttribute||(d=ay.createElement("div")),d.setAttribute&&d.removeAttribute&&(d.setAttribute(c,""),e=W(d[c],"function"),W(d[c],"undefined")||(d[c]=T),d.removeAttribute(c))),d=null,e}var a={select:"input",change:"input",submit:"form",reset:"form",error:"img",load:"img",abort:"img"};return b}(),P={}.hasOwnProperty,X;!W(P,"undefined")&&!W(P.call,"undefined")?X=function(a,b){return P.call(a,b)}:X=function(a,b){return b in a&&W(a.constructor.prototype[b],"undefined")},Function.prototype.bind||(Function.prototype.bind=function(a){var b=this;if(typeof b!="function"){throw new TypeError}var c=aq.call(arguments,1),d=function(){if(this instanceof d){var e=function(){};e.prototype=b.prototype;var f=new e,g=b.apply(f,c.concat(aq.call(arguments)));return Object(g)===g?g:f}return b.apply(a,c.concat(aq.call(arguments)))};return d}),am.flexbox=function(){return ad("flexWrap")},am.flexboxlegacy=function(){return ad("boxDirection")},am.canvas=function(){var a=ay.createElement("canvas");return !!a.getContext&&!!a.getContext("2d")},am.canvastext=function(){return !!aj.canvas&&!!W(ay.createElement("canvas").getContext("2d").fillText,"function")},am.webgl=function(){return !!av.WebGLRenderingContext},am.touch=function(){var a;return"ontouchstart" in av||av.DocumentTouch&&ay instanceof DocumentTouch?a=!0:at(["@media (",ac.join("touch-enabled),("),ax,")","{#modernizr{top:9px;position:absolute}}"].join(""),function(b){a=b.offsetTop===9}),a},am.geolocation=function(){return"geolocation" in navigator},am.postmessage=function(){return !!av.postMessage},am.websqldatabase=function(){return !!av.openDatabase},am.indexedDB=function(){return !!ad("indexedDB",av)},am.hashchange=function(){return aw("hashchange",av)&&(ay.documentMode===T||ay.documentMode>7)},am.history=function(){return !!av.history&&!!history.pushState},am.draganddrop=function(){var a=ay.createElement("div");return"draggable" in a||"ondragstart" in a&&"ondrop" in a},am.websockets=function(){return"WebSocket" in av||"MozWebSocket" in av},am.rgba=function(){return af("background-color:rgba(150,255,150,.5)"),ae(Z.backgroundColor,"rgba")},am.hsla=function(){return af("background-color:hsla(120,40%,100%,.5)"),ae(Z.backgroundColor,"rgba")||ae(Z.backgroundColor,"hsla")},am.multiplebgs=function(){return af("background:url(https://),url(https://),red url(https://)"),/(url\s*\(.*?){3}/.test(Z.background)},am.backgroundsize=function(){return ad("backgroundSize")},am.borderimage=function(){return ad("borderImage")},am.borderradius=function(){return ad("borderRadius")},am.boxshadow=function(){return ad("boxShadow")},am.textshadow=function(){return ay.createElement("div").style.textShadow===""},am.opacity=function(){return O("opacity:.55"),/^0.55$/.test(Z.opacity)},am.cssanimations=function(){return ad("animationName")},am.csscolumns=function(){return ad("columnCount")},am.cssgradients=function(){var a="background-image:",b="gradient(linear,left top,right bottom,from(#9f9),to(white));",c="linear-gradient(left top,#9f9, white);";return af((a+"-webkit- ".split(" ").join(b+a)+ac.join(c+a)).slice(0,-a.length)),ae(Z.backgroundImage,"gradient")},am.cssreflections=function(){return ad("boxReflect")},am.csstransforms=function(){return !!ad("transform")},am.csstransforms3d=function(){var a=!!ad("perspective");return a&&"webkitPerspective" in aa.style&&at("@media (transform-3d),(-webkit-transform-3d){#modernizr{left:9px;position:absolute;height:3px;}}",function(b,c){a=b.offsetLeft===9&&b.offsetHeight===3}),a},am.csstransitions=function(){return ad("transition")},am.fontface=function(){var a;return at('@font-face {font-family:"font";src:url("https://")}',function(b,c){var d=ay.getElementById("smodernizr"),e=d.sheet||d.styleSheet,f=e?e.cssRules&&e.cssRules[0]?e.cssRules[0].cssText:e.cssText||"":"";a=/src/i.test(f)&&f.indexOf(c.split(" ")[0])===0}),a},am.generatedcontent=function(){var a;return at(["#",ax,"{font:0/0 a}#",ax,':after{content:"',Q,'";visibility:hidden;font:3px/1 a}'].join(""),function(b){a=b.offsetHeight>=3}),a},am.video=function(){var a=ay.createElement("video"),b=!1;try{if(b=!!a.canPlayType){b=new Boolean(b),b.ogg=a.canPlayType('video/ogg; codecs="theora"').replace(/^no$/,""),b.h264=a.canPlayType('video/mp4; codecs="avc1.42E01E"').replace(/^no$/,""),b.webm=a.canPlayType('video/webm; codecs="vp8, vorbis"').replace(/^no$/,"")}}catch(c){}return b},am.audio=function(){var a=ay.createElement("audio"),b=!1;try{if(b=!!a.canPlayType){b=new Boolean(b),b.ogg=a.canPlayType('audio/ogg; codecs="vorbis"').replace(/^no$/,""),b.mp3=a.canPlayType("audio/mpeg;").replace(/^no$/,""),b.wav=a.canPlayType('audio/wav; codecs="1"').replace(/^no$/,""),b.m4a=(a.canPlayType("audio/x-m4a;")||a.canPlayType("audio/aac;")).replace(/^no$/,"")}}catch(c){}return b},am.localstorage=function(){try{return localStorage.setItem(ax,ax),localStorage.removeItem(ax),!0}catch(a){return !1}},am.sessionstorage=function(){try{return sessionStorage.setItem(ax,ax),sessionStorage.removeItem(ax),!0}catch(a){return !1}},am.webworkers=function(){return !!av.Worker},am.applicationcache=function(){return !!av.applicationCache},am.svg=function(){return !!ay.createElementNS&&!!ay.createElementNS(al.svg,"svg").createSVGRect},am.inlinesvg=function(){var a=ay.createElement("div");return a.innerHTML="<svg/>",(a.firstChild&&a.firstChild.namespaceURI)==al.svg},am.smil=function(){return !!ay.createElementNS&&/SVGAnimate/.test(Y.call(ay.createElementNS(al.svg,"animate")))},am.svgclippaths=function(){return !!ay.createElementNS&&/SVGClipPath/.test(Y.call(ay.createElementNS(al.svg,"clipPath")))};for(var U in am){X(am,U)&&(ar=U.toLowerCase(),aj[ar]=am[U](),ap.push((aj[ar]?"":"no-")+ar))}return aj.input||M(),aj.addTest=function(a,b){if(typeof a=="object"){for(var c in a){X(a,c)&&aj.addTest(c,a[c])}}else{a=a.toLowerCase();if(aj[a]!==T){return aj}b=typeof b=="function"?b():b,typeof S!="undefined"&&S&&(aa.className+=" "+(b?"":"no-")+a),aj[a]=b}return aj},af(""),R=ah=null,function(d,e){function o(t,u){var v=t.createElement("p"),w=t.getElementsByTagName("head")[0]||t.documentElement;return v.innerHTML="x<style>"+u+"</style>",w.insertBefore(v.lastChild,w.firstChild)}function p(){var t=c.elements;return typeof t=="string"?t.split(" "):t}function q(t){var u=m[t[k]];return u||(u={},l++,t[k]=l,m[l]=u),u}function r(t,u,v){u||(u=e);if(n){return u.createElement(t)}v||(v=q(u));var w;return v.cache[t]?w=v.cache[t].cloneNode():i.test(t)?w=(v.cache[t]=v.createElem(t)).cloneNode():w=v.createElem(t),w.canHaveChildren&&!h.test(t)&&!w.tagUrn?v.frag.appendChild(w):w}function s(t,u){t||(t=e);if(n){return t.createDocumentFragment()}u=u||q(t);var v=u.frag.cloneNode(),w=0,x=p(),y=x.length;for(;w<y;w++){v.createElement(x[w])}return v}function a(t,u){u.cache||(u.cache={},u.createElem=t.createElement,u.createFrag=t.createDocumentFragment,u.frag=u.createFrag()),t.createElement=function(v){return c.shivMethods?r(v,t,u):u.createElem(v)},t.createDocumentFragment=Function("h,f","return function(){var n=f.cloneNode(),c=n.createElement;h.shivMethods&&("+p().join().replace(/[\w\-]+/g,function(v){return u.createElem(v),u.frag.createElement(v),'c("'+v+'")'})+");return n}")(c,u.frag)}function b(t){t||(t=e);var u=q(t);return c.shivCSS&&!j&&!u.hasCSS&&(u.hasCSS=!!o(t,"article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}mark{background:#FF0;color:#000}template{display:none}")),n||a(t,u),t}var f="3.7.0",g=d.html5||{},h=/^<|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i,i=/^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i,j,k="_html5shiv",l=0,m={},n;(function(){try{var t=e.createElement("a");t.innerHTML="<xyz></xyz>",j="hidden" in t,n=t.childNodes.length==1||function(){e.createElement("a");var v=e.createDocumentFragment();return typeof v.cloneNode=="undefined"||typeof v.createDocumentFragment=="undefined"||typeof v.createElement=="undefined"}()}catch(u){j=!0,n=!0}})();var c={elements:g.elements||"abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output progress section summary template time video",version:f,shivCSS:g.shivCSS!==!1,supportsUnknownElements:n,shivMethods:g.shivMethods!==!1,type:"default",shivDocument:b,createElement:r,createDocumentFragment:s};d.html5=c,b(e)}(this,ay),aj._version=ab,aj._prefixes=ac,aj._domPrefixes=ak,aj._cssomPrefixes=ai,aj.mq=au,aj.hasEvent=aw,aj.testProp=function(a){return N([a])},aj.testAllProps=ad,aj.testStyles=at,aa.className=aa.className.replace(/(^|\s)no-js(\s|$)/,"$1$2")+(S?" js "+ap.join(" "):""),aj}(this,this.document),function(O,Q,S){function T(a){return"[object Function]"==D.call(a)}function U(a){return"string"==typeof a}function V(){}function W(a){return !a||"loaded"==a||"complete"==a||"uninitialized"==a}function X(){var a=F.shift();C=1,a?a.t?ac(function(){("c"==a.t?R.injectCss:R.injectJs)(a.s,0,a.a,a.x,a.e,1)},0):(a(),X()):C=0}function Y(a,b,c,d,e,f,g){function h(m){if(!j&&W(i.readyState)&&(l.r=j=1,!C&&X(),i.onload=i.onreadystatechange=null,m)){"img"!=a&&ac(function(){H.removeChild(i)},50);for(var n in M[b]){M[b].hasOwnProperty(n)&&M[b][n].onload()}}}var g=g||R.errorTimeout,i=Q.createElement(a),j=0,k=0,l={t:c,s:b,e:e,a:f,x:g};1===M[b]&&(k=1,M[b]=[]),"object"==a?i.data=b:(i.src=b,i.type=a),i.width=i.height="0",i.onerror=i.onload=i.onreadystatechange=function(){h.call(this,k)},F.splice(d,0,l),"img"!=a&&(k||2===M[b]?(H.insertBefore(i,G?null:ad),ac(h,g)):M[b].push(i))}function Z(a,b,c,d,e){return C=0,b=b||"j",U(a)?Y("c"==b?L:J,a,b,this.i++,c,d,e):(F.splice(this.i++,0,a),1==F.length&&X()),this}function aa(){var a=R;return a.loader={load:Z,i:0},a}var ab=Q.documentElement,ac=O.setTimeout,ad=Q.getElementsByTagName("script")[0],D={}.toString,F=[],C=0,E="MozAppearance" in ab.style,G=E&&!!Q.createRange().compareNode,H=G?ab:ad.parentNode,ab=O.opera&&"[object Opera]"==D.call(O.opera),ab=!!Q.attachEvent&&!ab,J=E?"object":ab?"script":"img",L=ab?"script":J,I=Array.isArray||function(a){return"[object Array]"==D.call(a)},K=[],M={},N={timeout:function(a,b){return b.length&&(a.timeout=b[0]),a}},P,R;R=function(a){function b(h){var h=h.split("!"),i=K.length,j=h.pop(),k=h.length,j={url:j,origUrl:j,prefixes:h},l,m,n;for(m=0;m<k;m++){n=h[m].split("="),(l=N[n.shift()])&&(j=l(j,n))}for(m=0;m<i;m++){j=K[m](j)}return j}function c(h,i,j,k,l){var m=b(h),n=m.autoCallback;m.url.split(".").pop().split("?").shift(),m.bypass||(i&&(i=T(i)?i:i[h]||i[k]||i[h.split("/").pop().split("?")[0]]),m.instead?m.instead(h,i,j,k,l):(M[m.url]?m.noexec=!0:M[m.url]=1,j.load(m.url,m.forceCSS||!m.forceJS&&"css"==m.url.split(".").pop().split("?").shift()?"c":S,m.noexec,m.attrs,m.timeout),(T(i)||T(n))&&j.load(function(){aa(),i&&i(m.origUrl,l,k),n&&n(m.origUrl,l,k),M[m.url]=2})))}function d(h,i){function j(r,s){if(r){if(U(r)){s||(m=function(){var t=[].slice.call(arguments);n.apply(this,t),o()}),c(r,m,i,0,k)}else{if(Object(r)===r){for(q in p=function(){var t=0,u;for(u in r){r.hasOwnProperty(u)&&t++}return t}(),r){r.hasOwnProperty(q)&&(!s&&!--p&&(T(m)?m=function(){var t=[].slice.call(arguments);n.apply(this,t),o()}:m[q]=function(t){return function(){var u=[].slice.call(arguments);t&&t.apply(this,u),o()}}(n[q])),c(r[q],m,i,q,k))}}}}else{!s&&o()}}var k=!!h.test,l=h.load||h.both,m=h.callback||V,n=m,o=h.complete||V,p,q;j(k?h.yep:h.nope,!!l),l&&j(l)}var e,f,g=this.yepnope.loader;if(U(a)){c(a,0,g,0)}else{if(I(a)){for(e=0;e<a.length;e++){f=a[e],U(f)?c(f,0,g,0):I(f)?R(f):Object(f)===f&&d(f,g)}}else{Object(a)===a&&d(a,g)}}},R.addPrefix=function(a,b){N[a]=b},R.addFilter=function(a){K.push(a)},R.errorTimeout=10000,null==Q.readyState&&Q.addEventListener&&(Q.readyState="loading",Q.addEventListener("DOMContentLoaded",P=function(){Q.removeEventListener("DOMContentLoaded",P,0),Q.readyState="complete"},0)),O.yepnope=aa(),O.yepnope.executeStack=X,O.yepnope.injectJs=function(a,b,c,d,e,f){var g=Q.createElement("script"),h,i,d=d||R.errorTimeout;g.src=a;for(i in c){g.setAttribute(i,c[i])}b=f?X:b||V,g.onreadystatechange=g.onload=function(){!h&&W(g.readyState)&&(h=1,b(),g.onload=g.onreadystatechange=null)},ac(function(){h||(h=1,b(1))},d),e?g.onload():ad.parentNode.insertBefore(g,ad)},O.yepnope.injectCss=function(a,b,c,d,e,f){var d=Q.createElement("link"),g,b=f?X:b||V;d.href=a,d.rel="stylesheet",d.type="text/css";for(g in c){d.setAttribute(g,c[g])}e||(ad.parentNode.insertBefore(d,ad),ac(b,0))}}(this,document),Modernizr.load=function(){yepnope.apply(window,[].slice.call(arguments,0))};
