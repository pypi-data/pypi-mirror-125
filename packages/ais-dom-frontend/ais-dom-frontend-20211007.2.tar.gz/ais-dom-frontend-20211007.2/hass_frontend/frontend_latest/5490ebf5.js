"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1804],{43709:(e,t,i)=>{var r=i(32421),s=i(7599),a=i(26767),o=i(5701),n=i(62359);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var s=t.placement;if(t.kind===r&&("static"===s||"prototype"===s)){var a="static"===s?e:i;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],s={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,s)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,s);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],s=e.decorators,a=s.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var n=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,s[a])(n)||n);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var d=c.extras;if(d){for(var l=0;l<d.length;l++)this.addElementPlacement(d[l],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var s=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(s)||s);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var n=o+1;n<e.length;n++)if(e[o].key===e[n].key&&e[o].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function y(e,t,i){return y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(r){var s=Object.getOwnPropertyDescriptor(r,t);return s.get?s.get.call(i):s.value}},y(e,t,i||e)}function v(e){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},v(e)}!function(e,t,i,r){var s=c();if(r)for(var a=0;a<r.length;a++)s=r[a](s);var o=t((function(e){s.initializeInstanceElements(e,n.elements)}),i),n=s.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var s,a=e[r];if("method"===a.kind&&(s=t.find(i)))if(u(a.descriptor)||u(s.descriptor)){if(p(a)||p(s))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");s.descriptor=a.descriptor}else{if(p(a)){if(p(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");s.decorators=a.decorators}l(a,s)}else t.push(a)}return t}(o.d.map(d)),e);s.initializeClassElements(o.F,n.elements),s.runClassFinishers(o.F,n.finishers)}([(0,a.M)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.C)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){y(v(i.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--switch-checked-color)"),this.addEventListener("change",(()=>{this.haptic&&(0,n.j)("light")}))}},{kind:"get",static:!0,key:"styles",value:function(){return[r.r.styles,s.iv`
        .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
          background-color: var(--switch-checked-button-color);
          border-color: var(--switch-checked-button-color);
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__track {
          background-color: var(--switch-checked-track-color);
          border-color: var(--switch-checked-track-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--switch-unchecked-button-color);
          border-color: var(--switch-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--switch-unchecked-track-color);
          border-color: var(--switch-unchecked-track-color);
        }
      `]}}]}}),r.r)},26765:(e,t,i)=>{i.d(t,{Ys:()=>o,g7:()=>n,D9:()=>c});var r=i(47181);const s=()=>Promise.all([i.e(68200),i.e(30879),i.e(29907),i.e(34831),i.e(1281)]).then(i.bind(i,1281)),a=(e,t,i)=>new Promise((a=>{const o=t.cancel,n=t.confirm;(0,r.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:s,dialogParams:{...t,...i,cancel:()=>{a(!(null==i||!i.prompt)&&null),o&&o()},confirm:e=>{a(null==i||!i.prompt||e),n&&n(e)}}})})),o=(e,t)=>a(e,t),n=(e,t)=>a(e,t,{confirmation:!0}),c=(e,t)=>a(e,t,{prompt:!0})},49412:(e,t,i)=>{i.r(t);i(53268),i(12730),i(27662),i(84281),i(62744),i(60010),i(38353),i(63081),i(43709),i(54909),i(55905);var r=i(7599),s=i(26767),a=i(5701),o=i(11654);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var s=t.placement;if(t.kind===r&&("static"===s||"prototype"===s)){var a="static"===s?e:i;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],s={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,s)}),this),e.forEach((function(e){if(!l(e))return i.push(e);var t=this.decorateElement(e,s);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],s=e.decorators,a=s.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var n=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,s[a])(n)||n);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var d=c.extras;if(d){for(var l=0;l<d.length;l++)this.addElementPlacement(d[l],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var s=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(s)||s);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var n=o+1;n<e.length;n++)if(e[o].key===e[n].key&&e[o].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function c(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var s=n();if(r)for(var a=0;a<r.length;a++)s=r[a](s);var o=t((function(e){s.initializeInstanceElements(e,u.elements)}),i),u=s.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var s,a=e[r];if("method"===a.kind&&(s=t.find(i)))if(p(a.descriptor)||p(s.descriptor)){if(l(a)||l(s))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");s.descriptor=a.descriptor}else{if(l(a)){if(l(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");s.decorators=a.decorators}d(a,s)}else t.push(a)}return t}(o.d.map(c)),e);s.initializeClassElements(o.F,u.elements),s.runClassFinishers(o.F,u.finishers)}([(0,s.M)("ha-config-ais-dom-config-update")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.C)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"field",decorators:[(0,a.C)({type:Boolean})],key:"validateConfigInProgress",value:()=>!1},{kind:"field",decorators:[(0,a.C)({type:String})],key:"validateLog",value:()=>""},{kind:"field",decorators:[(0,a.C)({type:String})],key:"aisButtonVersionCheckUpgrade",value:()=>""},{kind:"method",key:"firstUpdated",value:async function(){}},{kind:"method",key:"render",value:function(){return r.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header">Oprogramowanie bramki</span>
          <span slot="introduction"
            >Możesz zaktualizować system do najnowszej wersji, wykonać kopię
            zapasową ustawień i zsynchronizować bramkę z Portalem
            Integratora</span
          >
          <ha-card header="Wersja systemu AI-Speaker">
            <div class="card-content">
              <div
                style="color:${this._getTextColor(this.hass.states["sensor.version_info"])}"
              >
                ${this.hass.states["sensor.version_info"].state}
              </div>
              <div>
                <div style="margin-top:30px;" id="ha-switch-id">
                  <ha-switch
                    .checked=${"on"===this.hass.states["input_boolean.ais_auto_update"].state}
                    @change=${this.changeAutoUpdateMode}
                    style="position: absolute; right: 20px;"
                  ></ha-switch
                  ><span
                    ><h3>
                      Autoaktualizacja
                      <ha-icon
                        icon=${"on"===this.hass.states["input_boolean.ais_auto_update"].state?"mdi:sync":"mdi:sync-off"}
                      ></ha-icon></h3
                  ></span>
                </div>
              </div>

              <div style="display: inline-block;">
                <div>
                  ${"on"===this.hass.states["input_boolean.ais_auto_update"].state?r.dy`Codziennie sprawdzimy i automatycznie zainstalujemy
                      dostępne aktualizacje.`:r.dy`Możesz aktualizować system samodzielnie w dogodnym
                      dla Ciebie czasie lub włączyć aktualizację automatyczną.`}
                </div>
                <div style="margin-top: 15px;">
                  Aktualizacje dostarczają najnowsze funkcjonalności oraz
                  poprawki zapewniające bezpieczeństwo i stabilność działania
                  systemu.
                  <table style="margin-top: 10px;">
                    ${this.hass.states["sensor.version_info"].attributes.update_check_time?r.dy`<tr>
                          <td>
                            <ha-icon icon=""></ha-icon>
                            Sprawdzono o
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.update_check_time}
                          </td>
                          <td></td>
                          <td><ha-icon icon=""></ha-icon></td>
                        </tr>`:r.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.update_status?r.dy`<tr>
                          <td>
                            <ha-icon icon=""></ha-icon>
                            Status
                          </td>
                          <td>
                            ${this.getVersionName(this.hass.states["sensor.version_info"].attributes.update_status)}
                          </td>
                          <td></td>
                          <td>
                            <ha-icon
                              icon=${this.getVersionIcon(this.hass.states["sensor.version_info"].attributes.update_status)}
                            ></ha-icon>
                          </td>
                        </tr>`:r.dy``}
                    <tr style="height: 1em;"></tr>
                    ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_current_version?r.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:zigbee"></ha-icon>
                            Zigbee
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_zigbee2mqtt?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:r.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_current_version?r.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:home-assistant"></ha-icon>
                            AIS HA
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.dom_app_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.dom_app_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_dom_app?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:r.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.android_app_current_version?r.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:home-assistant"></ha-icon>
                            Android
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.android_app_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.android_app_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_android_app?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:r.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.linux_apt_current_version?r.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:linux"></ha-icon>
                            Linux
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.linux_apt_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.linux_apt_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_linux_apt?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:r.dy``}
                  </table>
                </div>
              </div>

              ${this._showUpdateButton(this.hass.states["sensor.version_info"])?r.dy` <div class="center-container">
                    <ha-call-service-button
                      class="warning"
                      .hass=${this.hass}
                      domain="ais_updater"
                      service="execute_upgrade"
                      .serviceData=${{say:!0}}
                    >
                      ${this._computeAisButtonVersionCheckUpgrade(this.hass.states["sensor.version_info"])}
                    </ha-call-service-button>
                  </div>`:r.dy`
                    <br /><br /><br />
                    ${this.hass.states["sensor.version_info"].attributes.progress?r.dy` <mwc-linear-progress
                          determinate
                          .progress=${this.hass.states["sensor.version_info"].attributes.progress}
                          .buffer=${this.hass.states["sensor.version_info"].attributes.buffer}
                        >
                        </mwc-linear-progress>`:r.dy`<mwc-linear-progress indeterminate>
                        </mwc-linear-progress>`}
                    <br />
                  `}
            </div>
          </ha-card>

          <ha-card header="Kopia konfiguracji Bramki">
            <div class="card-content">
              W tym miejscu możesz, sprawdzić poprawność ustawień bramki,
              wykonać jej kopię i przesłać ją do portalu integratora.
              <b
                >Uwaga, ponieważ konfiguracja może zawierać hasła i tokeny
                dostępu do usług, zalecamy zaszyfrować ją hasłem</b
              >. Gdy kopia jest zabezpieczona hasłem, to można ją
              otworzyć/przywrócić tylko po podaniu hasła.
              <h2>
                Nowa kopia ustawień
                <ha-icon icon="mdi:cloud-upload-outline"></ha-icon>
              </h2>
              <br />
              <div class="center-container">
                Kopia zapasowa ustawień:
                <br />
                <paper-radio-group selected="all" id="backup_type1">
                  <paper-radio-button name="all">Wszystkich</paper-radio-button>
                  <paper-radio-button name="ha">AIS HA</paper-radio-button>
                  <paper-radio-button name="zigbee">Zigbee</paper-radio-button>
                </paper-radio-group>
                <br />
                Przed wykonaniem nowej kopii ustawień sprawdź poprawność
                konfiguracji
              </div>
              <br />
              <div style="border-bottom: 1px solid white;">
                ${this.validateLog?r.dy`<div class="config-invalid">
                        <mwc-button raised="" @click=${this.doBackup}>
                          Popraw i sprawdź ponownie
                        </mwc-button>
                      </div>
                      <p></p>
                      <div id="configLog" class="validate-log">
                        ${this.validateLog}
                      </div>`:r.dy` <div class="validate-container">
                      <div class="validate-result" id="result">
                        ${this.hass.states["sensor.ais_backup_info"].attributes.backup_info}
                      </div>

                      ${this.validateConfigInProgress?r.dy`<mwc-linear-progress indeterminate>
                          </mwc-linear-progress>`:r.dy` <div class="config-invalid">
                              <span class="text">
                                ${this.hass.states["sensor.ais_backup_info"].attributes.backup_error}
                              </span>
                            </div>
                            ${"1"===this.hass.states["sensor.ais_backup_info"].state?r.dy`
                                  <paper-input
                                    placeholder="hasło"
                                    no-label-float=""
                                    type="password"
                                    id="password1"
                                  ></paper-input>
                                `:r.dy``}
                            <mwc-button raised="" @click=${this.doBackup}>
                              ${"0"===this.hass.states["sensor.ais_backup_info"].state?r.dy` Sprawdź konfigurację `:r.dy``}
                              ${"1"===this.hass.states["sensor.ais_backup_info"].state?r.dy` Wykonaj kopie konfiguracji `:r.dy``}
                            </mwc-button>`}
                    </div>`}
              </div>
              ${this.hass.states["sensor.ais_backup_info"].attributes.file_size||this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?r.dy` <h2>
                      Przywracanie ustawień
                      <ha-icon icon="mdi:backup-restore"></ha-icon>
                    </h2>
                    <div class="validate-container">
                      <table style="margin-top: 40px; margin-bottom: 10px;">
                      ${this.hass.states["sensor.ais_backup_info"].attributes.file_size?r.dy` <tr>
                              <td>
                                <ha-icon icon="mdi:home-assistant"></ha-icon>
                                AIS HA
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_name}
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_size}
                              </td>
                            </tr>`:r.dy``}
                      ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?r.dy` <tr>
                              <td>
                                <ha-icon icon="mdi:zigbee"></ha-icon>
                                Zigbee
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_name}
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size}
                              </td>
                            </tr>`:r.dy``}

                      </table>
                      <div class="validate-container">
                        <div class="validate-result" id="result">
                          ${this.hass.states["sensor.ais_backup_info"].attributes.restore_info}
                        </div>
                        <div class="config-invalid">
                              <span class="text">
                              ${this.hass.states["sensor.ais_backup_info"].attributes.restore_error}
                              </span>
                            </div>
                            Przywracanie ustawień z kopii:
                            <br />
                            <paper-radio-group selected="all" id="backup_type2">
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_size&&this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?r.dy`<paper-radio-button name="all"
                                        >Wszystkich</paper-radio-button
                                      >`:r.dy``}
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_size?r.dy`<paper-radio-button name="ha"
                                        >AIS HA</paper-radio-button
                                      >`:r.dy``}
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?r.dy`<paper-radio-button name="zigbee"
                                        >Zigbee</paper-radio-button
                                      >`:r.dy``}
                            </paper-radio-group>
                            <br />
                            <paper-input
                              placeholder="hasło"
                              no-label-float=""
                              type="password"
                              id="password2"
                            ></paper-input>
                            <mwc-button raised="" @click=${this.restoreBackup}>
                              Przywróć konfigurację z kopii
                            </mwc-button>
                          </div>
                      </div>
                    </div>`:r.dy``}
            </div>
          </ha-card>

          <ha-card header="Synchronizacja z Portalem Integratora">
            <div class="card-content">
              Jeśli ostatnio wprowadzałeś zmiany w Portalu Integratora, takie
              jak dodanie nowych typów audio czy też dostęp do zewnętrznych
              serwisów, to przyciskiem poniżej możesz uruchomić natychmiastowe
              pobranie tych zmian na bramkę bez czekania na automatyczną
              synchronizację.
              <div class="center-container">
                <ha-call-service-button
                  class="warning"
                  .hass=${this.hass}
                  domain="script"
                  service="ais_cloud_sync"
                  >Synchronizuj z Portalem Integratora
                </ha-call-service-button>
              </div>
            </div>
          </ha-card>
        </ha-config-section>
      </hass-subpage>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[o.Qx,r.iv`
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .center-container {
          text-align: center;
          margin-top: 2em;
          height: 70px;
        }
        table {
          width: 100%;
        }

        td:first-child {
          width: 33%;
        }

        .validate-container {
          text-align: center;
          min-height: 140px;
        }

        .validate-result {
          color: #0da035;
        }

        .config-invalid {
          text-align: center;
          margin-top: 2em;
          margin-bottom: 1em;
          color: #f44336;
        }

        .validate-log {
          white-space: pre-wrap;
          direction: ltr;
          color: #f44336;
        }
      `]}},{kind:"method",key:"getVersionName",value:function(e){let t=e;return"checking"===e?t="Sprawdzanie":"outdated"===e?t="Nieaktualny":"downloading"===e?t="Pobieranie":"installing"===e?t="Instalowanie":"updated"===e?t="Aktualny":"unknown"===e?t="Nieznany":"restart"===e&&(t="Restartowanie"),t}},{kind:"method",key:"getVersionIcon",value:function(e){let t="";return"checking"===e?t="mdi:cloud-sync":"outdated"===e?t="mdi:clock-alert-outline":"downloading"===e?t="mdi:progress-download":"installing"===e?t="mdi:progress-wrench":"updated"===e?t="mdi:emoticon-happy-outline":"unknown"===e?t="mdi:help-circle-outline":"restart"===e&&(t="mdi:restart-alert"),t}},{kind:"method",key:"_computeAisButtonVersionCheckUpgrade",value:function(e){const t=e.attributes;return t.reinstall_dom_app||t.reinstall_android_app||t.reinstall_linux_apt||t.reinstall_zigbee2mqtt?"outdated"===t.update_status?"Zainstaluj teraz aktualizację":"unknown"===t.update_status?"Spróbuj ponownie":"Aktualizacja -> "+this.getVersionName(t.update_status):"Sprawdź dostępność aktualizacji"}},{kind:"method",key:"_showUpdateButton",value:function(e){const t=e.attributes;return!(t.reinstall_dom_app||t.reinstall_android_app||t.reinstall_linux_apt||t.reinstall_zigbee2mqtt)||("outdated"===t.update_status||"unknown"===t.update_status)}},{kind:"method",key:"_getTextColor",value:function(e){const t=e.attributes;return t.reinstall_dom_app||t.reinstall_android_app||t.reinstall_linux_apt||t.reinstall_zigbee2mqtt?"outdated"===t.update_status?"#f44336":(t.update_status,"#ff9800"):"#0da035"}},{kind:"method",key:"changeAutoUpdateMode",value:function(){this.hass.callService("input_boolean","toggle",{entity_id:"input_boolean.ais_auto_update"})}},{kind:"method",key:"isBackupInProgress",value:function(e){return"0"!==e.state}},{kind:"method",key:"doBackup",value:function(){if("0"===this.hass.states["sensor.ais_backup_info"].state)this.validateConfigInProgress=!0,this.validateLog="",this.hass.callApi("POST","config/core/check_config").then((e=>{this.validateConfigInProgress=!1;const t="valid"===e.result?"1":"0";"0"===t?(this.hass.callService("ais_cloud","set_backup_step",{step:t,backup_error:"Konfiguracja niepoprawna"}),this.validateLog=e.errors):(this.hass.callService("ais_cloud","set_backup_step",{step:t,backup_info:"Konfiguracja poprawna można wykonać kopię"}),this.validateLog="")}));else{this.validateLog="";const e=this.shadowRoot.getElementById("password1").value,t=this.shadowRoot.getElementById("backup_type1").selected;this.hass.callService("ais_cloud","do_backup",{password:e,type:t})}}},{kind:"method",key:"restoreBackup",value:function(){this.validateLog="";const e=this.shadowRoot.getElementById("password2").value,t=this.shadowRoot.getElementById("backup_type2").selected;this.hass.callService("ais_cloud","restore_backup",{password:e,type:t})}}]}}),r.oi)}}]);
//# sourceMappingURL=5490ebf5.js.map