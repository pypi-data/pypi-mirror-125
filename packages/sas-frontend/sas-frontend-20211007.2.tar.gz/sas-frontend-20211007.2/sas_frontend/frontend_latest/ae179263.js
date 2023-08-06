"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[9928],{73826:(e,t,r)=>{r.d(t,{f:()=>m});var i=r(5701);function o(e,t,r,i){var o=n();if(i)for(var d=0;d<i.length;d++)o=i[d](o);var h=t((function(e){o.initializeInstanceElements(e,p.elements)}),r),p=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(l(n.descriptor)||l(o.descriptor)){if(c(n)||c(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(c(n)){if(c(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(h.d.map(a)),e);return o.initializeClassElements(h.F,p.elements),o.runClassFinishers(h.F,p.finishers)}function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=h(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function f(e,t,r){return f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=u(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}},f(e,t,r||e)}function u(e){return u=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},u(e)}const m=e=>o(null,(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){f(u(r.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if(f(u(r.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){f(u(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&(this.__unsubs=this.hassSubscribe())}}]}}),e)},9928:(e,t,r)=>{r.a(e,(async e=>{r.r(t);var i=r(7599),o=r(26767),n=r(5701),a=r(17717),s=r(228),c=(r(53918),r(18457)),l=(r(22098),r(52039),r(55424)),d=r(58763),h=r(73826),p=e([l,d]);function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!y(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return k(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?k(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=b(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function u(e){var t,r=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function y(e){return e.decorators&&e.decorators.length}function v(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function b(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function k(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}[l,d]=p.then?await p:p;const w=238.76104;!function(e,t,r,i){var o=f();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(v(n.descriptor)||v(o.descriptor)){if(y(n)||y(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(y(n)){if(y(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}m(n,o)}else t.push(n)}return t}(a.d.map(u)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,o.M)("hui-energy-distribution-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.S)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,a.S)()],key:"_data",value:void 0},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"hassSubscribe",value:function(){var e;return[(0,l.UB)(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"render",value:function(){var e,t;if(!this._config)return i.dy``;if(!this._data)return i.dy`Loading…`;const r=this._data.prefs,o=(0,l.Jj)(r),n=void 0!==o.solar,a=void 0!==o.battery,h=void 0!==o.gas,p=o.grid[0].flow_to.length>0,f=null!==(e=(0,d.q6)(this._data.stats,o.grid[0].flow_from.map((e=>e.stat_energy_from))))&&void 0!==e?e:0;let u=null;var m;h&&(u=null!==(m=(0,d.q6)(this._data.stats,o.gas.map((e=>e.stat_energy_from))))&&void 0!==m?m:0);let y=null;n&&(y=(0,d.q6)(this._data.stats,o.solar.map((e=>e.stat_energy_from)))||0);let v=null,g=null;a&&(v=(0,d.q6)(this._data.stats,o.battery.map((e=>e.stat_energy_to)))||0,g=(0,d.q6)(this._data.stats,o.battery.map((e=>e.stat_energy_from)))||0);let b=null;p&&(b=(0,d.q6)(this._data.stats,o.grid[0].flow_to.map((e=>e.stat_energy_to)))||0);let k=null;n&&(k=(y||0)-(b||0)-(v||0));let x=null,E=null;null!==k&&k<0&&(a&&(x=-1*k,x>f&&(E=Math.min(0,x-f),x=f)),k=0);let C=null;n&&a?(E||(E=Math.max(0,(b||0)-(y||0)-(v||0)-(x||0))),C=v-(x||0)):!n&&a&&(E=b);let $=null;a&&($=(g||0)-(E||0));const _=Math.max(0,f-(x||0)),P=Math.max(0,_+(k||0)+($||0));let L,M,D,S,H;n&&(L=w*(k/P)),$&&(M=w*($/P));let A="https://www.electricitymap.org";if(this._data.co2SignalEntity&&this._data.co2SignalEntity in this._data.stats){const e=(0,d.m2)(this._data.stats[this._data.co2SignalEntity],o.grid[0].flow_from.map((e=>this._data.stats[e.stat_energy_from])).filter(Boolean)),t=this.hass.states[this._data.co2SignalEntity];if(null!=t&&t.attributes.country_code&&(A+=`/zone/${t.attributes.country_code}`),null!==e){let t;D=f-e,t=_!==f?e*(_/f):e,H=w*(t/P),S=w-(L||0)-(M||0)-H}}const z=_+(k||0)+(b?b-(E||0):0)+(C||0)+($||0)+(x||0)+(E||0);return i.dy`
      <ha-card .header=${this._config.title}>
        <div class="card-content">
          ${void 0!==D||n||h?i.dy`<div class="row">
                ${void 0===D?i.dy`<div class="spacer"></div>`:i.dy`<div class="circle-container low-carbon">
                      <span class="label">Non-fossil</span>
                      <a
                        class="circle"
                        href=${A}
                        target="_blank"
                        rel="noopener no referrer"
                      >
                        <ha-svg-icon .path=${"M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"}></ha-svg-icon>
                        ${D?(0,c.u)(D,this.hass.locale,{maximumFractionDigits:1}):"-"}
                        kWh
                      </a>
                      <svg width="80" height="30">
                        <line x1="40" y1="0" x2="40" y2="30"></line>
                      </svg>
                    </div>`}
                ${n?i.dy`<div class="circle-container solar">
                      <span class="label">Solar</span>
                      <div class="circle">
                        <ha-svg-icon .path=${"M11.45,2V5.55L15,3.77L11.45,2M10.45,8L8,10.46L11.75,11.71L10.45,8M2,11.45L3.77,15L5.55,11.45H2M10,2H2V10C2.57,10.17 3.17,10.25 3.77,10.25C7.35,10.26 10.26,7.35 10.27,3.75C10.26,3.16 10.17,2.57 10,2M17,22V16H14L19,7V13H22L17,22Z"}></ha-svg-icon>
                        ${(0,c.u)(y||0,this.hass.locale,{maximumFractionDigits:1})}
                        kWh
                      </div>
                    </div>`:h?i.dy`<div class="spacer"></div>`:""}
                ${h?i.dy`<div class="circle-container gas">
                      <span class="label">Gas</span>
                      <div class="circle">
                        <ha-svg-icon .path=${"M17.66 11.2C17.43 10.9 17.15 10.64 16.89 10.38C16.22 9.78 15.46 9.35 14.82 8.72C13.33 7.26 13 4.85 13.95 3C13 3.23 12.17 3.75 11.46 4.32C8.87 6.4 7.85 10.07 9.07 13.22C9.11 13.32 9.15 13.42 9.15 13.55C9.15 13.77 9 13.97 8.8 14.05C8.57 14.15 8.33 14.09 8.14 13.93C8.08 13.88 8.04 13.83 8 13.76C6.87 12.33 6.69 10.28 7.45 8.64C5.78 10 4.87 12.3 5 14.47C5.06 14.97 5.12 15.47 5.29 15.97C5.43 16.57 5.7 17.17 6 17.7C7.08 19.43 8.95 20.67 10.96 20.92C13.1 21.19 15.39 20.8 17.03 19.32C18.86 17.66 19.5 15 18.56 12.72L18.43 12.46C18.22 12 17.66 11.2 17.66 11.2M14.5 17.5C14.22 17.74 13.76 18 13.4 18.1C12.28 18.5 11.16 17.94 10.5 17.28C11.69 17 12.4 16.12 12.61 15.23C12.78 14.43 12.46 13.77 12.33 13C12.21 12.26 12.23 11.63 12.5 10.94C12.69 11.32 12.89 11.7 13.13 12C13.9 13 15.11 13.44 15.37 14.8C15.41 14.94 15.43 15.08 15.43 15.23C15.46 16.05 15.1 16.95 14.5 17.5H14.5Z"}></ha-svg-icon>
                        ${(0,c.u)(u||0,this.hass.locale,{maximumFractionDigits:1})}
                        ${(0,l.vE)(this.hass,r)||"m³"}
                      </div>
                      <svg width="80" height="30">
                        <path d="M40 0 v30" id="gas" />
                        ${u?i.YP`<circle
                    r="1"
                    class="gas"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="2s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#gas" />
                    </animateMotion>
                  </circle>`:""}
                      </svg>
                    </div>`:i.dy`<div class="spacer"></div>`}
              </div>`:""}
          <div class="row">
            <div class="circle-container grid">
              <div class="circle">
                <ha-svg-icon .path=${"M8.28,5.45L6.5,4.55L7.76,2H16.23L17.5,4.55L15.72,5.44L15,4H9L8.28,5.45M18.62,8H14.09L13.3,5H10.7L9.91,8H5.38L4.1,10.55L5.89,11.44L6.62,10H17.38L18.1,11.45L19.89,10.56L18.62,8M17.77,22H15.7L15.46,21.1L12,15.9L8.53,21.1L8.3,22H6.23L9.12,11H11.19L10.83,12.35L12,14.1L13.16,12.35L12.81,11H14.88L17.77,22M11.4,15L10.5,13.65L9.32,18.13L11.4,15M14.68,18.12L13.5,13.64L12.6,15L14.68,18.12Z"}></ha-svg-icon>
                ${null!==b?i.dy`<span class="return">
                      <ha-svg-icon
                        class="small"
                        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
                      ></ha-svg-icon
                      >${(0,c.u)(b,this.hass.locale,{maximumFractionDigits:1})}
                      kWh
                    </span>`:""}
                <span class="consumption">
                  ${p?i.dy`<ha-svg-icon
                        class="small"
                        .path=${"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"}
                      ></ha-svg-icon>`:""}${(0,c.u)(f,this.hass.locale,{maximumFractionDigits:1})}
                  kWh
                </span>
              </div>
              <span class="label">Grid</span>
            </div>
            <div class="circle-container home">
              <div
                class="circle ${(0,s.$)({border:void 0===L&&void 0===S})}"
              >
                <ha-svg-icon .path=${"M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"}></ha-svg-icon>
                ${(0,c.u)(P,this.hass.locale,{maximumFractionDigits:1})}
                kWh
                ${void 0!==L||void 0!==S?i.dy`<svg>
                      ${void 0!==L?i.YP`<circle
                            class="solar"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${L} ${w-L}"
                            shape-rendering="geometricPrecision"
                            stroke-dashoffset="-${w-L}"
                          />`:""}
                      ${M?i.YP`<circle
                            class="battery"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${M} ${w-M}"
                            stroke-dashoffset="-${w-M-(L||0)}"
                            shape-rendering="geometricPrecision"
                          />`:""}
                      ${S?i.YP`<circle
                            class="low-carbon"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${S} ${w-S}"
                            stroke-dashoffset="-${w-S-(M||0)-(L||0)}"
                            shape-rendering="geometricPrecision"
                          />`:""}
                      <circle
                        class="grid"
                        cx="40"
                        cy="40"
                        r="38"
                        stroke-dasharray="${null!==(t=H)&&void 0!==t?t:w-L-(M||0)} ${void 0!==H?w-H:L+(M||0)}"
                        stroke-dashoffset="0"
                        shape-rendering="geometricPrecision"
                      />
                    </svg>`:""}
              </div>
              <span class="label">Home</span>
            </div>
          </div>
          ${a?i.dy`<div class="row">
                <div class="spacer"></div>
                <div class="circle-container battery">
                  <div class="circle">
                    <ha-svg-icon .path=${"M16 20H8V6H16M16.67 4H15V2H9V4H7.33C6.6 4 6 4.6 6 5.33V20.67C6 21.4 6.6 22 7.33 22H16.67C17.41 22 18 21.41 18 20.67V5.33C18 4.6 17.4 4 16.67 4M15 16H9V19H15V16M15 7H9V10H15V7M15 11.5H9V14.5H15V11.5Z"}></ha-svg-icon>
                    <span class="battery-in">
                      <ha-svg-icon
                        class="small"
                        .path=${"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z"}
                      ></ha-svg-icon
                      >${(0,c.u)(v||0,this.hass.locale,{maximumFractionDigits:1})}
                      kWh</span
                    >
                    <span class="battery-out">
                      <ha-svg-icon
                        class="small"
                        .path=${"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}
                      ></ha-svg-icon>
                      ${(0,c.u)(g||0,this.hass.locale,{maximumFractionDigits:1})}
                      kWh</span
                    >
                  </div>
                  <span class="label">Battery</span>
                </div>
                <div class="spacer"></div>
              </div>`:""}
          <div class="lines ${(0,s.$)({battery:a})}">
            <svg
              viewBox="0 0 100 100"
              xmlns="http://www.w3.org/2000/svg"
              preserveAspectRatio="xMidYMid slice"
            >
              ${p&&n?i.YP`<path
                    id="return"
                    class="return"
                    d="M${a?45:47},0 v15 c0,${a?"35 -10,30 -30,30":"40 -10,35 -30,35"} h-20"
                    vector-effect="non-scaling-stroke"
                  ></path> `:""}
              ${n?i.YP`<path
                    id="solar"
                    class="solar"
                    d="M${a?55:53},0 v15 c0,${a?"35 10,30 30,30":"40 10,35 30,35"} h20"
                    vector-effect="non-scaling-stroke"
                  ></path>`:""}
              ${a?i.YP`<path
                    id="battery-house"
                    class="battery-house"
                    d="M55,100 v-15 c0,-35 10,-30 30,-30 h20"
                    vector-effect="non-scaling-stroke"
                  ></path>
                  <path
                    id="battery-grid"
                    class=${(0,s.$)({"battery-from-grid":Boolean(x),"battery-to-grid":Boolean(E)})}
                    d="M45,100 v-15 c0,-35 -10,-30 -30,-30 h-20"
                    vector-effect="non-scaling-stroke"
                  ></path>
                  `:""}
              ${a&&n?i.YP`<path
                    id="battery-solar"
                    class="battery-solar"
                    d="M50,0 V100"
                    vector-effect="non-scaling-stroke"
                  ></path>`:""}
              <path
                class="grid"
                id="grid"
                d="M0,${a?50:n?56:53} H100"
                vector-effect="non-scaling-stroke"
              ></path>
              ${b&&n?i.YP`<circle
                    r="1"
                    class="return"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-(b-(E||0))/z*6}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#return" />
                    </animateMotion>
                  </circle>`:""}
              ${k?i.YP`<circle
                    r="1"
                    class="solar"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-k/z*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#solar" />
                    </animateMotion>
                  </circle>`:""}
              ${_?i.YP`<circle
                    r="1"
                    class="grid"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-_/z*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#grid" />
                    </animateMotion>
                  </circle>`:""}
              ${C?i.YP`<circle
                    r="1"
                    class="battery-solar"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-C/z*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-solar" />
                    </animateMotion>
                  </circle>`:""}
              ${$?i.YP`<circle
                    r="1"
                    class="battery-house"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-$/z*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-house" />
                    </animateMotion>
                  </circle>`:""}
              ${x?i.YP`<circle
                    r="1"
                    class="battery-from-grid"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-x/z*5}s"
                      repeatCount="indefinite"
                      keyPoints="1;0" keyTimes="0;1"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-grid" />
                    </animateMotion>
                  </circle>`:""}
              ${E?i.YP`<circle
                    r="1"
                    class="battery-to-grid"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-E/z*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-grid" />
                    </animateMotion>
                  </circle>`:""}
            </svg>
          </div>
        </div>
        ${this._config.link_dashboard?i.dy`
              <div class="card-actions">
                <a href="/energy"
                  ><mwc-button> Go to the energy dashboard </mwc-button></a
                >
              </div>
            `:""}
      </ha-card>
    `}},{kind:"field",static:!0,key:"styles",value:()=>i.iv`
    :host {
      --mdc-icon-size: 24px;
    }
    .card-content {
      position: relative;
    }
    .lines {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 146px;
      display: flex;
      justify-content: center;
      padding: 0 16px 16px;
      box-sizing: border-box;
    }
    .lines.battery {
      bottom: 100px;
      height: 156px;
    }
    .lines svg {
      width: calc(100% - 160px);
      height: 100%;
      max-width: 340px;
    }
    .row {
      display: flex;
      justify-content: space-between;
      max-width: 500px;
      margin: 0 auto;
    }
    .circle-container {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .circle-container.low-carbon {
      margin-right: 4px;
    }
    .circle-container.solar {
      margin: 0 4px;
      height: 130px;
    }
    .circle-container.gas {
      margin-left: 4px;
      height: 130px;
    }
    .circle-container.battery {
      height: 110px;
      justify-content: flex-end;
    }
    .spacer {
      width: 84px;
    }
    .circle {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      box-sizing: border-box;
      border: 2px solid;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-size: 12px;
      line-height: 12px;
      position: relative;
      text-decoration: none;
      color: var(--primary-text-color);
    }
    ha-svg-icon {
      padding-bottom: 2px;
    }
    ha-svg-icon.small {
      --mdc-icon-size: 12px;
    }
    .label {
      color: var(--secondary-text-color);
      font-size: 12px;
    }
    line,
    path {
      stroke: var(--primary-text-color);
      stroke-width: 1;
      fill: none;
    }
    .circle svg {
      position: absolute;
      fill: none;
      stroke-width: 4px;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
    }
    .gas path,
    .gas circle {
      stroke: var(--energy-gas-color);
    }
    circle.gas {
      stroke-width: 4;
      fill: var(--energy-gas-color);
    }
    .gas .circle {
      border-color: var(--energy-gas-color);
    }
    .low-carbon line {
      stroke: var(--energy-non-fossil-color);
    }
    .low-carbon .circle {
      border-color: var(--energy-non-fossil-color);
    }
    .low-carbon ha-svg-icon {
      color: var(--energy-non-fossil-color);
    }
    circle.low-carbon {
      stroke: var(--energy-non-fossil-color);
      fill: var(--energy-non-fossil-color);
    }
    .solar .circle {
      border-color: var(--energy-solar-color);
    }
    circle.solar,
    path.solar {
      stroke: var(--energy-solar-color);
    }
    circle.solar {
      stroke-width: 4;
      fill: var(--energy-solar-color);
    }
    .battery .circle {
      border-color: var(--energy-battery-in-color);
    }
    circle.battery,
    path.battery {
      stroke: var(--energy-battery-out-color);
    }
    path.battery-house,
    circle.battery-house {
      stroke: var(--energy-battery-out-color);
    }
    circle.battery-house {
      stroke-width: 4;
      fill: var(--energy-battery-out-color);
    }
    path.battery-solar,
    circle.battery-solar {
      stroke: var(--energy-battery-in-color);
    }
    circle.battery-solar {
      stroke-width: 4;
      fill: var(--energy-battery-in-color);
    }
    .battery-in {
      color: var(--energy-battery-in-color);
    }
    .battery-out {
      color: var(--energy-battery-out-color);
    }
    path.battery-from-grid {
      stroke: var(--energy-grid-consumption-color);
    }
    path.battery-to-grid {
      stroke: var(--energy-grid-return-color);
    }
    path.return,
    circle.return,
    circle.battery-to-grid {
      stroke: var(--energy-grid-return-color);
    }
    circle.return,
    circle.battery-to-grid {
      stroke-width: 4;
      fill: var(--energy-grid-return-color);
    }
    .return {
      color: var(--energy-grid-return-color);
    }
    .grid .circle {
      border-color: var(--energy-grid-consumption-color);
    }
    .consumption {
      color: var(--energy-grid-consumption-color);
    }
    circle.grid,
    circle.battery-from-grid,
    path.grid {
      stroke: var(--energy-grid-consumption-color);
    }
    circle.grid,
    circle.battery-from-grid {
      stroke-width: 4;
      fill: var(--energy-grid-consumption-color);
    }
    .home .circle {
      border-width: 0;
      border-color: var(--primary-color);
    }
    .home .circle.border {
      border-width: 2px;
    }
    .circle svg circle {
      animation: rotate-in 0.6s ease-in;
      transition: stroke-dashoffset 0.4s, stroke-dasharray 0.4s;
      fill: none;
    }
    @keyframes rotate-in {
      from {
        stroke-dashoffset: 238.76104;
        stroke-dasharray: 238.76104;
      }
    }
    .card-actions a {
      text-decoration: none;
    }
  `}]}}),(0,h.f)(i.oi))}))}}]);
//# sourceMappingURL=ae179263.js.map