/*! For license information please see f4f19070.js.LICENSE.txt */
"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[54188],{65660:(e,t,r)=>{r(65233);const n=r(50856).d`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content);var s=document.createElement("style");s.textContent="[hidden] { display: none !important; }",document.head.appendChild(s)},15495:(e,t,r)=>{r(65233);const n=r(50856).d`
<custom-style>
  <style is="custom-style">
    html {

      /* Material Design color palette for Google products */

      --google-red-100: #f4c7c3;
      --google-red-300: #e67c73;
      --google-red-500: #db4437;
      --google-red-700: #c53929;

      --google-blue-100: #c6dafc;
      --google-blue-300: #7baaf7;
      --google-blue-500: #4285f4;
      --google-blue-700: #3367d6;

      --google-green-100: #b7e1cd;
      --google-green-300: #57bb8a;
      --google-green-500: #0f9d58;
      --google-green-700: #0b8043;

      --google-yellow-100: #fce8b2;
      --google-yellow-300: #f7cb4d;
      --google-yellow-500: #f4b400;
      --google-yellow-700: #f09300;

      --google-grey-100: #f5f5f5;
      --google-grey-300: #e0e0e0;
      --google-grey-500: #9e9e9e;
      --google-grey-700: #616161;

      /* Material Design color palette from online spec document */

      --paper-red-50: #ffebee;
      --paper-red-100: #ffcdd2;
      --paper-red-200: #ef9a9a;
      --paper-red-300: #e57373;
      --paper-red-400: #ef5350;
      --paper-red-500: #f44336;
      --paper-red-600: #e53935;
      --paper-red-700: #d32f2f;
      --paper-red-800: #c62828;
      --paper-red-900: #b71c1c;
      --paper-red-a100: #ff8a80;
      --paper-red-a200: #ff5252;
      --paper-red-a400: #ff1744;
      --paper-red-a700: #d50000;

      --paper-pink-50: #fce4ec;
      --paper-pink-100: #f8bbd0;
      --paper-pink-200: #f48fb1;
      --paper-pink-300: #f06292;
      --paper-pink-400: #ec407a;
      --paper-pink-500: #e91e63;
      --paper-pink-600: #d81b60;
      --paper-pink-700: #c2185b;
      --paper-pink-800: #ad1457;
      --paper-pink-900: #880e4f;
      --paper-pink-a100: #ff80ab;
      --paper-pink-a200: #ff4081;
      --paper-pink-a400: #f50057;
      --paper-pink-a700: #c51162;

      --paper-purple-50: #f3e5f5;
      --paper-purple-100: #e1bee7;
      --paper-purple-200: #ce93d8;
      --paper-purple-300: #ba68c8;
      --paper-purple-400: #ab47bc;
      --paper-purple-500: #9c27b0;
      --paper-purple-600: #8e24aa;
      --paper-purple-700: #7b1fa2;
      --paper-purple-800: #6a1b9a;
      --paper-purple-900: #4a148c;
      --paper-purple-a100: #ea80fc;
      --paper-purple-a200: #e040fb;
      --paper-purple-a400: #d500f9;
      --paper-purple-a700: #aa00ff;

      --paper-deep-purple-50: #ede7f6;
      --paper-deep-purple-100: #d1c4e9;
      --paper-deep-purple-200: #b39ddb;
      --paper-deep-purple-300: #9575cd;
      --paper-deep-purple-400: #7e57c2;
      --paper-deep-purple-500: #673ab7;
      --paper-deep-purple-600: #5e35b1;
      --paper-deep-purple-700: #512da8;
      --paper-deep-purple-800: #4527a0;
      --paper-deep-purple-900: #311b92;
      --paper-deep-purple-a100: #b388ff;
      --paper-deep-purple-a200: #7c4dff;
      --paper-deep-purple-a400: #651fff;
      --paper-deep-purple-a700: #6200ea;

      --paper-indigo-50: #e8eaf6;
      --paper-indigo-100: #c5cae9;
      --paper-indigo-200: #9fa8da;
      --paper-indigo-300: #7986cb;
      --paper-indigo-400: #5c6bc0;
      --paper-indigo-500: #3f51b5;
      --paper-indigo-600: #3949ab;
      --paper-indigo-700: #303f9f;
      --paper-indigo-800: #283593;
      --paper-indigo-900: #1a237e;
      --paper-indigo-a100: #8c9eff;
      --paper-indigo-a200: #536dfe;
      --paper-indigo-a400: #3d5afe;
      --paper-indigo-a700: #304ffe;

      --paper-blue-50: #e3f2fd;
      --paper-blue-100: #bbdefb;
      --paper-blue-200: #90caf9;
      --paper-blue-300: #64b5f6;
      --paper-blue-400: #42a5f5;
      --paper-blue-500: #2196f3;
      --paper-blue-600: #1e88e5;
      --paper-blue-700: #1976d2;
      --paper-blue-800: #1565c0;
      --paper-blue-900: #0d47a1;
      --paper-blue-a100: #82b1ff;
      --paper-blue-a200: #448aff;
      --paper-blue-a400: #2979ff;
      --paper-blue-a700: #2962ff;

      --paper-light-blue-50: #e1f5fe;
      --paper-light-blue-100: #b3e5fc;
      --paper-light-blue-200: #81d4fa;
      --paper-light-blue-300: #4fc3f7;
      --paper-light-blue-400: #29b6f6;
      --paper-light-blue-500: #03a9f4;
      --paper-light-blue-600: #039be5;
      --paper-light-blue-700: #0288d1;
      --paper-light-blue-800: #0277bd;
      --paper-light-blue-900: #01579b;
      --paper-light-blue-a100: #80d8ff;
      --paper-light-blue-a200: #40c4ff;
      --paper-light-blue-a400: #00b0ff;
      --paper-light-blue-a700: #0091ea;

      --paper-cyan-50: #e0f7fa;
      --paper-cyan-100: #b2ebf2;
      --paper-cyan-200: #80deea;
      --paper-cyan-300: #4dd0e1;
      --paper-cyan-400: #26c6da;
      --paper-cyan-500: #00bcd4;
      --paper-cyan-600: #00acc1;
      --paper-cyan-700: #0097a7;
      --paper-cyan-800: #00838f;
      --paper-cyan-900: #006064;
      --paper-cyan-a100: #84ffff;
      --paper-cyan-a200: #18ffff;
      --paper-cyan-a400: #00e5ff;
      --paper-cyan-a700: #00b8d4;

      --paper-teal-50: #e0f2f1;
      --paper-teal-100: #b2dfdb;
      --paper-teal-200: #80cbc4;
      --paper-teal-300: #4db6ac;
      --paper-teal-400: #26a69a;
      --paper-teal-500: #009688;
      --paper-teal-600: #00897b;
      --paper-teal-700: #00796b;
      --paper-teal-800: #00695c;
      --paper-teal-900: #004d40;
      --paper-teal-a100: #a7ffeb;
      --paper-teal-a200: #64ffda;
      --paper-teal-a400: #1de9b6;
      --paper-teal-a700: #00bfa5;

      --paper-green-50: #e8f5e9;
      --paper-green-100: #c8e6c9;
      --paper-green-200: #a5d6a7;
      --paper-green-300: #81c784;
      --paper-green-400: #66bb6a;
      --paper-green-500: #4caf50;
      --paper-green-600: #43a047;
      --paper-green-700: #388e3c;
      --paper-green-800: #2e7d32;
      --paper-green-900: #1b5e20;
      --paper-green-a100: #b9f6ca;
      --paper-green-a200: #69f0ae;
      --paper-green-a400: #00e676;
      --paper-green-a700: #00c853;

      --paper-light-green-50: #f1f8e9;
      --paper-light-green-100: #dcedc8;
      --paper-light-green-200: #c5e1a5;
      --paper-light-green-300: #aed581;
      --paper-light-green-400: #9ccc65;
      --paper-light-green-500: #8bc34a;
      --paper-light-green-600: #7cb342;
      --paper-light-green-700: #689f38;
      --paper-light-green-800: #558b2f;
      --paper-light-green-900: #33691e;
      --paper-light-green-a100: #ccff90;
      --paper-light-green-a200: #b2ff59;
      --paper-light-green-a400: #76ff03;
      --paper-light-green-a700: #64dd17;

      --paper-lime-50: #f9fbe7;
      --paper-lime-100: #f0f4c3;
      --paper-lime-200: #e6ee9c;
      --paper-lime-300: #dce775;
      --paper-lime-400: #d4e157;
      --paper-lime-500: #cddc39;
      --paper-lime-600: #c0ca33;
      --paper-lime-700: #afb42b;
      --paper-lime-800: #9e9d24;
      --paper-lime-900: #827717;
      --paper-lime-a100: #f4ff81;
      --paper-lime-a200: #eeff41;
      --paper-lime-a400: #c6ff00;
      --paper-lime-a700: #aeea00;

      --paper-yellow-50: #fffde7;
      --paper-yellow-100: #fff9c4;
      --paper-yellow-200: #fff59d;
      --paper-yellow-300: #fff176;
      --paper-yellow-400: #ffee58;
      --paper-yellow-500: #ffeb3b;
      --paper-yellow-600: #fdd835;
      --paper-yellow-700: #fbc02d;
      --paper-yellow-800: #f9a825;
      --paper-yellow-900: #f57f17;
      --paper-yellow-a100: #ffff8d;
      --paper-yellow-a200: #ffff00;
      --paper-yellow-a400: #ffea00;
      --paper-yellow-a700: #ffd600;

      --paper-amber-50: #fff8e1;
      --paper-amber-100: #ffecb3;
      --paper-amber-200: #ffe082;
      --paper-amber-300: #ffd54f;
      --paper-amber-400: #ffca28;
      --paper-amber-500: #ffc107;
      --paper-amber-600: #ffb300;
      --paper-amber-700: #ffa000;
      --paper-amber-800: #ff8f00;
      --paper-amber-900: #ff6f00;
      --paper-amber-a100: #ffe57f;
      --paper-amber-a200: #ffd740;
      --paper-amber-a400: #ffc400;
      --paper-amber-a700: #ffab00;

      --paper-orange-50: #fff3e0;
      --paper-orange-100: #ffe0b2;
      --paper-orange-200: #ffcc80;
      --paper-orange-300: #ffb74d;
      --paper-orange-400: #ffa726;
      --paper-orange-500: #ff9800;
      --paper-orange-600: #fb8c00;
      --paper-orange-700: #f57c00;
      --paper-orange-800: #ef6c00;
      --paper-orange-900: #e65100;
      --paper-orange-a100: #ffd180;
      --paper-orange-a200: #ffab40;
      --paper-orange-a400: #ff9100;
      --paper-orange-a700: #ff6500;

      --paper-deep-orange-50: #fbe9e7;
      --paper-deep-orange-100: #ffccbc;
      --paper-deep-orange-200: #ffab91;
      --paper-deep-orange-300: #ff8a65;
      --paper-deep-orange-400: #ff7043;
      --paper-deep-orange-500: #ff5722;
      --paper-deep-orange-600: #f4511e;
      --paper-deep-orange-700: #e64a19;
      --paper-deep-orange-800: #d84315;
      --paper-deep-orange-900: #bf360c;
      --paper-deep-orange-a100: #ff9e80;
      --paper-deep-orange-a200: #ff6e40;
      --paper-deep-orange-a400: #ff3d00;
      --paper-deep-orange-a700: #dd2c00;

      --paper-brown-50: #efebe9;
      --paper-brown-100: #d7ccc8;
      --paper-brown-200: #bcaaa4;
      --paper-brown-300: #a1887f;
      --paper-brown-400: #8d6e63;
      --paper-brown-500: #795548;
      --paper-brown-600: #6d4c41;
      --paper-brown-700: #5d4037;
      --paper-brown-800: #4e342e;
      --paper-brown-900: #3e2723;

      --paper-grey-50: #fafafa;
      --paper-grey-100: #f5f5f5;
      --paper-grey-200: #eeeeee;
      --paper-grey-300: #e0e0e0;
      --paper-grey-400: #bdbdbd;
      --paper-grey-500: #9e9e9e;
      --paper-grey-600: #757575;
      --paper-grey-700: #616161;
      --paper-grey-800: #424242;
      --paper-grey-900: #212121;

      --paper-blue-grey-50: #eceff1;
      --paper-blue-grey-100: #cfd8dc;
      --paper-blue-grey-200: #b0bec5;
      --paper-blue-grey-300: #90a4ae;
      --paper-blue-grey-400: #78909c;
      --paper-blue-grey-500: #607d8b;
      --paper-blue-grey-600: #546e7a;
      --paper-blue-grey-700: #455a64;
      --paper-blue-grey-800: #37474f;
      --paper-blue-grey-900: #263238;

      /* opacity for dark text on a light background */
      --dark-divider-opacity: 0.12;
      --dark-disabled-opacity: 0.38; /* or hint text or icon */
      --dark-secondary-opacity: 0.54;
      --dark-primary-opacity: 0.87;

      /* opacity for light text on a dark background */
      --light-divider-opacity: 0.12;
      --light-disabled-opacity: 0.3; /* or hint text or icon */
      --light-secondary-opacity: 0.7;
      --light-primary-opacity: 1.0;

    }

  </style>
</custom-style>
`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content)},1656:(e,t,r)=>{r(65233),r(15495);const n=r(50856).d`
<custom-style>
  <style is="custom-style">
    html {
      /*
       * You can use these generic variables in your elements for easy theming.
       * For example, if all your elements use \`--primary-text-color\` as its main
       * color, then switching from a light to a dark theme is just a matter of
       * changing the value of \`--primary-text-color\` in your application.
       */
      --primary-text-color: var(--light-theme-text-color);
      --primary-background-color: var(--light-theme-background-color);
      --secondary-text-color: var(--light-theme-secondary-color);
      --disabled-text-color: var(--light-theme-disabled-color);
      --divider-color: var(--light-theme-divider-color);
      --error-color: var(--paper-deep-orange-a700);

      /*
       * Primary and accent colors. Also see color.js for more colors.
       */
      --primary-color: var(--paper-indigo-500);
      --light-primary-color: var(--paper-indigo-100);
      --dark-primary-color: var(--paper-indigo-700);

      --accent-color: var(--paper-pink-a200);
      --light-accent-color: var(--paper-pink-a100);
      --dark-accent-color: var(--paper-pink-a400);


      /*
       * Material Design Light background theme
       */
      --light-theme-background-color: #ffffff;
      --light-theme-base-color: #000000;
      --light-theme-text-color: var(--paper-grey-900);
      --light-theme-secondary-color: #737373;  /* for secondary text and icons */
      --light-theme-disabled-color: #9b9b9b;  /* disabled/hint text */
      --light-theme-divider-color: #dbdbdb;

      /*
       * Material Design Dark background theme
       */
      --dark-theme-background-color: var(--paper-grey-900);
      --dark-theme-base-color: #ffffff;
      --dark-theme-text-color: #ffffff;
      --dark-theme-secondary-color: #bcbcbc;  /* for secondary text and icons */
      --dark-theme-disabled-color: #646464;  /* disabled/hint text */
      --dark-theme-divider-color: #3c3c3c;

      /*
       * Deprecated values because of their confusing names.
       */
      --text-primary-color: var(--dark-theme-text-color);
      --default-primary-color: var(--primary-color);
    }
  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content)},54242:(e,t,r)=>{r(65233);const n=r(50856).d`
<custom-style>
  <style is="custom-style">
    html {

      --shadow-transition: {
        transition: box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1);
      };

      --shadow-none: {
        box-shadow: none;
      };

      /* from http://codepen.io/shyndman/pen/c5394ddf2e8b2a5c9185904b57421cdb */

      --shadow-elevation-2dp: {
        box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14),
                    0 1px 5px 0 rgba(0, 0, 0, 0.12),
                    0 3px 1px -2px rgba(0, 0, 0, 0.2);
      };

      --shadow-elevation-3dp: {
        box-shadow: 0 3px 4px 0 rgba(0, 0, 0, 0.14),
                    0 1px 8px 0 rgba(0, 0, 0, 0.12),
                    0 3px 3px -2px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-4dp: {
        box-shadow: 0 4px 5px 0 rgba(0, 0, 0, 0.14),
                    0 1px 10px 0 rgba(0, 0, 0, 0.12),
                    0 2px 4px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-6dp: {
        box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14),
                    0 1px 18px 0 rgba(0, 0, 0, 0.12),
                    0 3px 5px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-8dp: {
        box-shadow: 0 8px 10px 1px rgba(0, 0, 0, 0.14),
                    0 3px 14px 2px rgba(0, 0, 0, 0.12),
                    0 5px 5px -3px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-12dp: {
        box-shadow: 0 12px 16px 1px rgba(0, 0, 0, 0.14),
                    0 4px 22px 3px rgba(0, 0, 0, 0.12),
                    0 6px 7px -4px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-16dp: {
        box-shadow: 0 16px 24px 2px rgba(0, 0, 0, 0.14),
                    0  6px 30px 5px rgba(0, 0, 0, 0.12),
                    0  8px 10px -5px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-24dp: {
        box-shadow: 0 24px 38px 3px rgba(0, 0, 0, 0.14),
                    0 9px 46px 8px rgba(0, 0, 0, 0.12),
                    0 11px 15px -7px rgba(0, 0, 0, 0.4);
      };
    }
  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content)},47686:(e,t,r)=>{r(65233);if(!window.polymerSkipLoadingFontRoboto){const e=document.createElement("link");e.rel="stylesheet",e.type="text/css",e.crossOrigin="anonymous",e.href="https://fonts.googleapis.com/css?family=Roboto+Mono:400,700|Roboto:400,300,300italic,400italic,500,500italic,700,700italic",document.head.appendChild(e)}const n=r(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content)},37961:(e,t,r)=>{var n=r(28426),s=r(76389),i=r(4507),a=r(36608);let o=(0,s.o)((e=>{let t=(0,a.SH)(e);return class extends t{static get properties(){return{items:{type:Array},multi:{type:Boolean,value:!1},selected:{type:Object,notify:!0},selectedItem:{type:Object,notify:!0},toggle:{type:Boolean,value:!1}}}static get observers(){return["__updateSelection(multi, items.*)"]}constructor(){super(),this.__lastItems=null,this.__lastMulti=null,this.__selectedMap=null}__updateSelection(e,t){let r=t.path;if(r==JSCompiler_renameProperty("items",this)){let r=t.base||[],n=this.__lastItems;if(e!==this.__lastMulti&&this.clearSelection(),n){let e=(0,i.c)(r,n);this.__applySplices(e)}this.__lastItems=r,this.__lastMulti=e}else if(t.path==`${JSCompiler_renameProperty("items",this)}.splices`)this.__applySplices(t.value.indexSplices);else{let e=r.slice(`${JSCompiler_renameProperty("items",this)}.`.length),t=parseInt(e,10);e.indexOf(".")<0&&e==t&&this.__deselectChangedIdx(t)}}__applySplices(e){let t=this.__selectedMap;for(let r=0;r<e.length;r++){let n=e[r];t.forEach(((e,r)=>{e<n.index||(e>=n.index+n.removed.length?t.set(r,e+n.addedCount-n.removed.length):t.set(r,-1))}));for(let e=0;e<n.addedCount;e++){let r=n.index+e;t.has(this.items[r])&&t.set(this.items[r],r)}}this.__updateLinks();let r=0;t.forEach(((e,n)=>{e<0?(this.multi?this.splice(JSCompiler_renameProperty("selected",this),r,1):this.selected=this.selectedItem=null,t.delete(n)):r++}))}__updateLinks(){if(this.__dataLinkedPaths={},this.multi){let e=0;this.__selectedMap.forEach((t=>{t>=0&&this.linkPaths(`${JSCompiler_renameProperty("items",this)}.${t}`,`${JSCompiler_renameProperty("selected",this)}.${e++}`)}))}else this.__selectedMap.forEach((e=>{this.linkPaths(JSCompiler_renameProperty("selected",this),`${JSCompiler_renameProperty("items",this)}.${e}`),this.linkPaths(JSCompiler_renameProperty("selectedItem",this),`${JSCompiler_renameProperty("items",this)}.${e}`)}))}clearSelection(){this.__dataLinkedPaths={},this.__selectedMap=new Map,this.selected=this.multi?[]:null,this.selectedItem=null}isSelected(e){return this.__selectedMap.has(e)}isIndexSelected(e){return this.isSelected(this.items[e])}__deselectChangedIdx(e){let t=this.__selectedIndexForItemIndex(e);if(t>=0){let e=0;this.__selectedMap.forEach(((r,n)=>{t==e++&&this.deselect(n)}))}}__selectedIndexForItemIndex(e){let t=this.__dataLinkedPaths[`${JSCompiler_renameProperty("items",this)}.${e}`];if(t)return parseInt(t.slice(`${JSCompiler_renameProperty("selected",this)}.`.length),10)}deselect(e){let t=this.__selectedMap.get(e);if(t>=0){let r;this.__selectedMap.delete(e),this.multi&&(r=this.__selectedIndexForItemIndex(t)),this.__updateLinks(),this.multi?this.splice(JSCompiler_renameProperty("selected",this),r,1):this.selected=this.selectedItem=null}}deselectIndex(e){this.deselect(this.items[e])}select(e){this.selectIndex(this.items.indexOf(e))}selectIndex(e){let t=this.items[e];this.isSelected(t)?this.toggle&&this.deselectIndex(e):(this.multi||this.__selectedMap.clear(),this.__selectedMap.set(t,e),this.__updateLinks(),this.multi?this.push(JSCompiler_renameProperty("selected",this),t):this.selected=this.selectedItem=t)}}}))(n.H3);class l extends o{static get is(){return"array-selector"}static get template(){return null}}customElements.define(l.is,l)},5618:(e,t,r)=>{var n=r(34816),s=r(10868),i=r(26539);const a=new n.ZP;window.ShadyCSS||(window.ShadyCSS={prepareTemplate(e,t,r){},prepareTemplateDom(e,t){},prepareTemplateStyles(e,t,r){},styleSubtree(e,t){a.processStyles(),(0,s.wW)(e,t)},styleElement(e){a.processStyles()},styleDocument(e){a.processStyles(),(0,s.wW)(document.body,e)},getComputedStyleValue:(e,t)=>(0,s.B7)(e,t),flushCustomStyles(){},nativeCss:i.rd,nativeShadow:i.WA,cssBuild:i.Cp,disableRuntime:i.jF}),window.ShadyCSS.CustomStyleInterface=a;var o=r(15392);const l="include",p=window.ShadyCSS.CustomStyleInterface;class d extends HTMLElement{constructor(){super(),this._style=null,p.addCustomStyle(this)}getStyle(){if(this._style)return this._style;const e=this.querySelector("style");if(!e)return null;this._style=e;const t=e.getAttribute(l);return t&&(e.removeAttribute(l),e.textContent=(0,o.jv)(t)+e.textContent),this.ownerDocument!==window.document&&window.document.head.appendChild(this),this._style}}window.customElements.define("custom-style",d)},9024:(e,t,r)=>{r(56646);var n=r(40729),s=r(18691),i=r(60995),a=r(74460),o=r(62276),l=r(6226);const p=(0,i._)((0,s.w)((0,n.q)(HTMLElement)));customElements.define("dom-bind",class extends p{static get observedAttributes(){return["mutable-data"]}constructor(){if(super(),a.XN)throw new Error("strictTemplatePolicy: dom-bind not allowed");this.root=null,this.$=null,this.__children=null}attributeChangedCallback(e,t,r,n){this.mutableData=!0}connectedCallback(){(0,l.N)()||(this.style.display="none"),this.render()}disconnectedCallback(){this.__removeChildren()}__insertChildren(){(0,o.r)((0,o.r)(this).parentNode).insertBefore(this.root,this)}__removeChildren(){if(this.__children)for(let e=0;e<this.__children.length;e++)this.root.appendChild(this.__children[e])}render(){let e;if(!this.__children){if(e=e||this.querySelector("template"),!e){let t=new MutationObserver((()=>{if(e=this.querySelector("template"),!e)throw new Error("dom-bind requires a <template> child");t.disconnect(),this.render()}));return void t.observe(this,{childList:!0})}this.root=this._stampTemplate(e),this.$=this.root.$,this.__children=[];for(let e=this.root.firstChild;e;e=e.nextSibling)this.__children[this.__children.length]=e;this._enableProperties()}this.__insertChildren(),this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0}))}})},26047:(e,t,r)=>{var n=r(28426),s=r(78956),i=r(93252),a=r(21683),o=r(4059),l=r(62276),p=r(6226),d=r(74460),c=r(52521);class h extends n.H3{static get is(){return"dom-if"}static get template(){return null}static get properties(){return{if:{type:Boolean,observer:"__debounceRender"},restamp:{type:Boolean,observer:"__debounceRender"},notifyDomChange:{type:Boolean}}}constructor(){super(),this.__renderDebouncer=null,this._lastIf=!1,this.__hideTemplateChildren__=!1,this.__template,this._templateInfo}__debounceRender(){this.__renderDebouncer=s.dx.debounce(this.__renderDebouncer,a.YA,(()=>this.__render())),(0,i.E)(this.__renderDebouncer)}disconnectedCallback(){super.disconnectedCallback();const e=(0,l.r)(this).parentNode;e&&(e.nodeType!=Node.DOCUMENT_FRAGMENT_NODE||(0,l.r)(e).host)||this.__teardownInstance()}connectedCallback(){super.connectedCallback(),(0,p.N)()||(this.style.display="none"),this.if&&this.__debounceRender()}__ensureTemplate(){if(!this.__template){const e=this;let t=e._templateInfo?e:(0,l.r)(e).querySelector("template");if(!t){let e=new MutationObserver((()=>{if(!(0,l.r)(this).querySelector("template"))throw new Error("dom-if requires a <template> child");e.disconnect(),this.__render()}));return e.observe(this,{childList:!0}),!1}this.__template=t}return!0}__ensureInstance(){let e=(0,l.r)(this).parentNode;if(this.__hasInstance()){let t=this.__getInstanceNodes();if(t&&t.length){if((0,l.r)(this).previousSibling!==t[t.length-1])for(let r,n=0;n<t.length&&(r=t[n]);n++)(0,l.r)(e).insertBefore(r,this)}}else{if(!e)return!1;if(!this.__ensureTemplate())return!1;this.__createAndInsertInstance(e)}return!0}render(){(0,i.y)()}__render(){if(this.if){if(!this.__ensureInstance())return}else this.restamp&&this.__teardownInstance();this._showHideChildren(),d.dJ&&!this.notifyDomChange||this.if==this._lastIf||(this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0})),this._lastIf=this.if)}__hasInstance(){}__getInstanceNodes(){}__createAndInsertInstance(e){}__teardownInstance(){}_showHideChildren(){}}const u=d.ew?class extends h{constructor(){super(),this.__instance=null,this.__syncInfo=null}__hasInstance(){return Boolean(this.__instance)}__getInstanceNodes(){return this.__instance.templateInfo.childNodes}__createAndInsertInstance(e){const t=this.__dataHost||this;if(d.XN&&!this.__dataHost)throw new Error("strictTemplatePolicy: template owner not trusted");const r=t._bindTemplate(this.__template,!0);r.runEffects=(e,t,r)=>{let n=this.__syncInfo;if(this.if)n&&(this.__syncInfo=null,this._showHideChildren(),t=Object.assign(n.changedProps,t)),e(t,r);else if(this.__instance)if(n||(n=this.__syncInfo={runEffects:e,changedProps:{}}),r)for(const e in t){const t=(0,o.Jz)(e);n.changedProps[t]=this.__dataHost[t]}else Object.assign(n.changedProps,t)},this.__instance=t._stampTemplate(this.__template,r),(0,l.r)(e).insertBefore(this.__instance,this)}__syncHostProperties(){const e=this.__syncInfo;e&&(this.__syncInfo=null,e.runEffects(e.changedProps,!1))}__teardownInstance(){const e=this.__dataHost||this;this.__instance&&(e._removeBoundDom(this.__instance),this.__instance=null,this.__syncInfo=null)}_showHideChildren(){const e=this.__hideTemplateChildren__||!this.if;this.__instance&&Boolean(this.__instance.__hidden)!==e&&(this.__instance.__hidden=e,(0,c.aZ)(e,this.__instance.templateInfo.childNodes)),e||this.__syncHostProperties()}}:class extends h{constructor(){super(),this.__ctor=null,this.__instance=null,this.__invalidProps=null}__hasInstance(){return Boolean(this.__instance)}__getInstanceNodes(){return this.__instance.children}__createAndInsertInstance(e){this.__ctor||(this.__ctor=(0,c.Uv)(this.__template,this,{mutableData:!0,forwardHostProp:function(e,t){this.__instance&&(this.if?this.__instance.forwardHostProp(e,t):(this.__invalidProps=this.__invalidProps||Object.create(null),this.__invalidProps[(0,o.Jz)(e)]=!0))}})),this.__instance=new this.__ctor,(0,l.r)(e).insertBefore(this.__instance.root,this)}__teardownInstance(){if(this.__instance){let e=this.__instance.children;if(e&&e.length){let t=(0,l.r)(e[0]).parentNode;if(t){t=(0,l.r)(t);for(let r,n=0;n<e.length&&(r=e[n]);n++)t.removeChild(r)}}this.__invalidProps=null,this.__instance=null}}__syncHostProperties(){let e=this.__invalidProps;if(e){this.__invalidProps=null;for(let t in e)this.__instance._setPendingProperty(t,this.__dataHost[t]);this.__instance._flushProperties()}}_showHideChildren(){const e=this.__hideTemplateChildren__||!this.if;this.__instance&&Boolean(this.__instance.__hidden)!==e&&(this.__instance.__hidden=e,this.__instance._showHideChildren(e)),e||this.__syncHostProperties()}};customElements.define(u.is,u)},42173:(e,t,r)=>{var n=r(28426),s=r(52521),i=r(78956),a=r(93252),o=r(18691),l=r(4059),p=r(21683),d=r(62276),c=r(6226),h=r(74460);const u=(0,o.w)(n.H3);class _ extends u{static get is(){return"dom-repeat"}static get template(){return null}static get properties(){return{items:{type:Array},as:{type:String,value:"item"},indexAs:{type:String,value:"index"},itemsIndexAs:{type:String,value:"itemsIndex"},sort:{type:Function,observer:"__sortChanged"},filter:{type:Function,observer:"__filterChanged"},observe:{type:String,observer:"__observeChanged"},delay:Number,renderedItemCount:{type:Number,notify:!h.dJ,readOnly:!0},initialCount:{type:Number},targetFramerate:{type:Number,value:20},_targetFrameTime:{type:Number,computed:"__computeFrameTime(targetFramerate)"},notifyDomChange:{type:Boolean},reuseChunkedInstances:{type:Boolean}}}static get observers(){return["__itemsChanged(items.*)"]}constructor(){super(),this.__instances=[],this.__renderDebouncer=null,this.__itemsIdxToInstIdx={},this.__chunkCount=null,this.__renderStartTime=null,this.__itemsArrayChanged=!1,this.__shouldMeasureChunk=!1,this.__shouldContinueChunking=!1,this.__chunkingId=0,this.__sortFn=null,this.__filterFn=null,this.__observePaths=null,this.__ctor=null,this.__isDetached=!0,this.template=null,this._templateInfo}disconnectedCallback(){super.disconnectedCallback(),this.__isDetached=!0;for(let e=0;e<this.__instances.length;e++)this.__detachInstance(e)}connectedCallback(){if(super.connectedCallback(),(0,c.N)()||(this.style.display="none"),this.__isDetached){this.__isDetached=!1;let e=(0,d.r)((0,d.r)(this).parentNode);for(let t=0;t<this.__instances.length;t++)this.__attachInstance(t,e)}}__ensureTemplatized(){if(!this.__ctor){const e=this;let t=this.template=e._templateInfo?e:this.querySelector("template");if(!t){let e=new MutationObserver((()=>{if(!this.querySelector("template"))throw new Error("dom-repeat requires a <template> child");e.disconnect(),this.__render()}));return e.observe(this,{childList:!0}),!1}let r={};r[this.as]=!0,r[this.indexAs]=!0,r[this.itemsIndexAs]=!0,this.__ctor=(0,s.Uv)(t,this,{mutableData:this.mutableData,parentModel:!0,instanceProps:r,forwardHostProp:function(e,t){let r=this.__instances;for(let n,s=0;s<r.length&&(n=r[s]);s++)n.forwardHostProp(e,t)},notifyInstanceProp:function(e,t,r){if((0,l.wB)(this.as,t)){let n=e[this.itemsIndexAs];t==this.as&&(this.items[n]=r);let s=(0,l.Iu)(this.as,`${JSCompiler_renameProperty("items",this)}.${n}`,t);this.notifyPath(s,r)}}})}return!0}__getMethodHost(){return this.__dataHost._methodHost||this.__dataHost}__functionFromPropertyValue(e){if("string"==typeof e){let t=e,r=this.__getMethodHost();return function(){return r[t].apply(r,arguments)}}return e}__sortChanged(e){this.__sortFn=this.__functionFromPropertyValue(e),this.items&&this.__debounceRender(this.__render)}__filterChanged(e){this.__filterFn=this.__functionFromPropertyValue(e),this.items&&this.__debounceRender(this.__render)}__computeFrameTime(e){return Math.ceil(1e3/e)}__observeChanged(){this.__observePaths=this.observe&&this.observe.replace(".*",".").split(" ")}__handleObservedPaths(e){if(this.__sortFn||this.__filterFn)if(e){if(this.__observePaths){let t=this.__observePaths;for(let r=0;r<t.length;r++)0===e.indexOf(t[r])&&this.__debounceRender(this.__render,this.delay)}}else this.__debounceRender(this.__render,this.delay)}__itemsChanged(e){this.items&&!Array.isArray(this.items)&&console.warn("dom-repeat expected array for `items`, found",this.items),this.__handleItemPath(e.path,e.value)||("items"===e.path&&(this.__itemsArrayChanged=!0),this.__debounceRender(this.__render))}__debounceRender(e,t=0){this.__renderDebouncer=i.dx.debounce(this.__renderDebouncer,t>0?p.Wc.after(t):p.YA,e.bind(this)),(0,a.E)(this.__renderDebouncer)}render(){this.__debounceRender(this.__render),(0,a.y)()}__render(){if(!this.__ensureTemplatized())return;let e=this.items||[];const t=this.__sortAndFilterItems(e),r=this.__calculateLimit(t.length);this.__updateInstances(e,r,t),this.initialCount&&(this.__shouldMeasureChunk||this.__shouldContinueChunking)&&(cancelAnimationFrame(this.__chunkingId),this.__chunkingId=requestAnimationFrame((()=>this.__continueChunking()))),this._setRenderedItemCount(this.__instances.length),h.dJ&&!this.notifyDomChange||this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0}))}__sortAndFilterItems(e){let t=new Array(e.length);for(let r=0;r<e.length;r++)t[r]=r;return this.__filterFn&&(t=t.filter(((t,r,n)=>this.__filterFn(e[t],r,n)))),this.__sortFn&&t.sort(((t,r)=>this.__sortFn(e[t],e[r]))),t}__calculateLimit(e){let t=e;const r=this.__instances.length;if(this.initialCount){let n;!this.__chunkCount||this.__itemsArrayChanged&&!this.reuseChunkedInstances?(t=Math.min(e,this.initialCount),n=Math.max(t-r,0),this.__chunkCount=n||1):(n=Math.min(Math.max(e-r,0),this.__chunkCount),t=Math.min(r+n,e)),this.__shouldMeasureChunk=n===this.__chunkCount,this.__shouldContinueChunking=t<e,this.__renderStartTime=performance.now()}return this.__itemsArrayChanged=!1,t}__continueChunking(){if(this.__shouldMeasureChunk){const e=performance.now()-this.__renderStartTime,t=this._targetFrameTime/e;this.__chunkCount=Math.round(this.__chunkCount*t)||1}this.__shouldContinueChunking&&this.__debounceRender(this.__render)}__updateInstances(e,t,r){const n=this.__itemsIdxToInstIdx={};let s;for(s=0;s<t;s++){let t=this.__instances[s],i=r[s],a=e[i];n[i]=s,t?(t._setPendingProperty(this.as,a),t._setPendingProperty(this.indexAs,s),t._setPendingProperty(this.itemsIndexAs,i),t._flushProperties()):this.__insertInstance(a,s,i)}for(let e=this.__instances.length-1;e>=s;e--)this.__detachAndRemoveInstance(e)}__detachInstance(e){let t=this.__instances[e];const r=(0,d.r)(t.root);for(let e=0;e<t.children.length;e++){let n=t.children[e];r.appendChild(n)}return t}__attachInstance(e,t){let r=this.__instances[e];t.insertBefore(r.root,this)}__detachAndRemoveInstance(e){this.__detachInstance(e),this.__instances.splice(e,1)}__stampInstance(e,t,r){let n={};return n[this.as]=e,n[this.indexAs]=t,n[this.itemsIndexAs]=r,new this.__ctor(n)}__insertInstance(e,t,r){const n=this.__stampInstance(e,t,r);let s=this.__instances[t+1],i=s?s.children[0]:this;return(0,d.r)((0,d.r)(this).parentNode).insertBefore(n.root,i),this.__instances[t]=n,n}_showHideChildren(e){for(let t=0;t<this.__instances.length;t++)this.__instances[t]._showHideChildren(e)}__handleItemPath(e,t){let r=e.slice(6),n=r.indexOf("."),s=n<0?r:r.substring(0,n);if(s==parseInt(s,10)){let e=n<0?"":r.substring(n+1);this.__handleObservedPaths(e);let i=this.__itemsIdxToInstIdx[s],a=this.__instances[i];if(a){let r=this.as+(e?"."+e:"");a._setPendingPropertyOrPath(r,t,!1,!0),a._flushProperties()}return!0}}itemForElement(e){let t=this.modelForElement(e);return t&&t[this.as]}indexForElement(e){let t=this.modelForElement(e);return t&&t[this.indexAs]}modelForElement(e){return(0,s.GJ)(this.template,e)}}customElements.define(_.is,_)},18890:(e,t,r)=>{r.d(t,{x:()=>Pe});var n=r(26539);class s{constructor(){this.start=0,this.end=0,this.previous=null,this.parent=null,this.rules=null,this.parsedCssText="",this.cssText="",this.atRule=!1,this.type=0,this.keyframesName="",this.selector="",this.parsedSelector=""}}function i(e){return a(function(e){let t=new s;t.start=0,t.end=e.length;let r=t;for(let n=0,i=e.length;n<i;n++)if(e[n]===p){r.rules||(r.rules=[]);let e=r,t=e.rules[e.rules.length-1]||null;r=new s,r.start=n+1,r.parent=e,r.previous=t,e.rules.push(r)}else e[n]===d&&(r.end=n+1,r=r.parent||t);return t}(e=e.replace(c.comments,"").replace(c.port,"")),e)}function a(e,t){let r=t.substring(e.start,e.end-1);if(e.parsedCssText=e.cssText=r.trim(),e.parent){let n=e.previous?e.previous.end:e.parent.start;r=t.substring(n,e.start-1),r=function(e){return e.replace(/\\([0-9a-f]{1,6})\s/gi,(function(){let e=arguments[1],t=6-e.length;for(;t--;)e="0"+e;return"\\"+e}))}(r),r=r.replace(c.multipleSpaces," "),r=r.substring(r.lastIndexOf(";")+1);let s=e.parsedSelector=e.selector=r.trim();e.atRule=0===s.indexOf(_),e.atRule?0===s.indexOf(u)?e.type=l.MEDIA_RULE:s.match(c.keyframesRule)&&(e.type=l.KEYFRAMES_RULE,e.keyframesName=e.selector.split(c.multipleSpaces).pop()):0===s.indexOf(h)?e.type=l.MIXIN_RULE:e.type=l.STYLE_RULE}let n=e.rules;if(n)for(let e,r=0,s=n.length;r<s&&(e=n[r]);r++)a(e,t);return e}function o(e,t,r=""){let n="";if(e.cssText||e.rules){let r=e.rules;if(r&&!function(e){let t=e[0];return Boolean(t)&&Boolean(t.selector)&&0===t.selector.indexOf(h)}(r))for(let e,s=0,i=r.length;s<i&&(e=r[s]);s++)n=o(e,t,n);else n=t?e.cssText:function(e){return function(e){return e.replace(c.mixinApply,"").replace(c.varApply,"")}(e=function(e){return e.replace(c.customProp,"").replace(c.mixinProp,"")}(e))}(e.cssText),n=n.trim(),n&&(n="  "+n+"\n")}return n&&(e.selector&&(r+=e.selector+" "+p+"\n"),r+=n,e.selector&&(r+=d+"\n\n")),r}const l={STYLE_RULE:1,KEYFRAMES_RULE:7,MEDIA_RULE:4,MIXIN_RULE:1e3},p="{",d="}",c={comments:/\/\*[^*]*\*+([^/*][^*]*\*+)*\//gim,port:/@import[^;]*;/gim,customProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?(?:[;\n]|$)/gim,mixinProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?{[^}]*?}(?:[;\n]|$)?/gim,mixinApply:/@apply\s*\(?[^);]*\)?\s*(?:[;\n]|$)?/gim,varApply:/[^;:]*?:[^;]*?var\([^;]*\)(?:[;\n]|$)?/gim,keyframesRule:/^@[^\s]*keyframes/,multipleSpaces:/\s+/g},h="--",u="@media",_="@";var f=r(60309);const m=new Set;function y(e){const t=e.textContent;if(!m.has(t)){m.add(t);const e=document.createElement("style");e.setAttribute("shady-unscoped",""),e.textContent=t,document.head.appendChild(e)}}function g(e){return e.hasAttribute("shady-unscoped")}function b(e,t){return e?("string"==typeof e&&(e=i(e)),t&&w(e,t),o(e,n.rd)):""}function C(e){return!e.__cssRules&&e.textContent&&(e.__cssRules=i(e.textContent)),e.__cssRules||null}function w(e,t,r,n){if(!e)return;let s=!1,i=e.type;if(n&&i===l.MEDIA_RULE){let t=e.selector.match(f.mA);t&&(window.matchMedia(t[1]).matches||(s=!0))}i===l.STYLE_RULE?t(e):r&&i===l.KEYFRAMES_RULE?r(e):i===l.MIXIN_RULE&&(s=!0);let a=e.rules;if(a&&!s)for(let e,s=0,i=a.length;s<i&&(e=a[s]);s++)w(e,t,r,n)}function x(e,t){let r=0;for(let n=t,s=e.length;n<s;n++)if("("===e[n])r++;else if(")"===e[n]&&0==--r)return n;return-1}function P(e,t){let r=e.indexOf("var(");if(-1===r)return t(e,"","","");let n=x(e,r+3),s=e.substring(r+4,n),i=e.substring(0,r),a=P(e.substring(n+1),t),o=s.indexOf(",");return-1===o?t(i,s.trim(),"",a):t(i,s.substring(0,o).trim(),s.substring(o+1).trim(),a)}window.ShadyDOM&&window.ShadyDOM.wrap;const S="css-build";function v(e){if(void 0!==n.Cp)return n.Cp;if(void 0===e.__cssBuild){const t=e.getAttribute(S);if(t)e.__cssBuild=t;else{const t=function(e){const t="template"===e.localName?e.content.firstChild:e.firstChild;if(t instanceof Comment){const e=t.textContent.trim().split(":");if(e[0]===S)return e[1]}return""}(e);""!==t&&function(e){const t="template"===e.localName?e.content.firstChild:e.firstChild;t.parentNode.removeChild(t)}(e),e.__cssBuild=t}}return e.__cssBuild||""}function E(e){return""!==v(e)}var A=r(10868);const O=/;\s*/m,T=/^\s*(initial)|(inherit)\s*$/,k=/\s*!important/,I="_-_";class N{constructor(){this._map={}}set(e,t){e=e.trim(),this._map[e]={properties:t,dependants:{}}}get(e){return e=e.trim(),this._map[e]||null}}let R=null;class M{constructor(){this._currentElement=null,this._measureElement=null,this._map=new N}detectMixin(e){return(0,A.OH)(e)}gatherStyles(e){const t=function(e){const t=[],r=e.querySelectorAll("style");for(let e=0;e<r.length;e++){const s=r[e];g(s)?n.WA||(y(s),s.parentNode.removeChild(s)):(t.push(s.textContent),s.parentNode.removeChild(s))}return t.join("").trim()}(e.content);if(t){const r=document.createElement("style");return r.textContent=t,e.content.insertBefore(r,e.content.firstChild),r}return null}transformTemplate(e,t){void 0===e._gatheredStyle&&(e._gatheredStyle=this.gatherStyles(e));const r=e._gatheredStyle;return r?this.transformStyle(r,t):null}transformStyle(e,t=""){let r=C(e);return this.transformRules(r,t),e.textContent=b(r),r}transformCustomStyle(e){let t=C(e);return w(t,(e=>{":root"===e.selector&&(e.selector="html"),this.transformRule(e)})),e.textContent=b(t),t}transformRules(e,t){this._currentElement=t,w(e,(e=>{this.transformRule(e)})),this._currentElement=null}transformRule(e){e.cssText=this.transformCssText(e.parsedCssText,e),":root"===e.selector&&(e.selector=":host > *")}transformCssText(e,t){return e=e.replace(f.CN,((e,r,n,s)=>this._produceCssProperties(e,r,n,s,t))),this._consumeCssProperties(e,t)}_getInitialValueForProperty(e){return this._measureElement||(this._measureElement=document.createElement("meta"),this._measureElement.setAttribute("apply-shim-measure",""),this._measureElement.style.all="initial",document.head.appendChild(this._measureElement)),window.getComputedStyle(this._measureElement).getPropertyValue(e)}_fallbacksFromPreviousRules(e){let t=e;for(;t.parent;)t=t.parent;const r={};let n=!1;return w(t,(t=>{n=n||t===e,n||t.selector===e.selector&&Object.assign(r,this._cssTextToMap(t.parsedCssText))})),r}_consumeCssProperties(e,t){let r=null;for(;r=f.$T.exec(e);){let n=r[0],s=r[1],i=r.index,a=i+n.indexOf("@apply"),o=i+n.length,l=e.slice(0,a),p=e.slice(o),d=t?this._fallbacksFromPreviousRules(t):{};Object.assign(d,this._cssTextToMap(l));let c=this._atApplyToCssProperties(s,d);e=`${l}${c}${p}`,f.$T.lastIndex=i+c.length}return e}_atApplyToCssProperties(e,t){e=e.replace(O,"");let r=[],n=this._map.get(e);if(n||(this._map.set(e,{}),n=this._map.get(e)),n){let s,i,a;this._currentElement&&(n.dependants[this._currentElement]=!0);const o=n.properties;for(s in o)a=t&&t[s],i=[s,": var(",e,I,s],a&&i.push(",",a.replace(k,"")),i.push(")"),k.test(o[s])&&i.push(" !important"),r.push(i.join(""))}return r.join("; ")}_replaceInitialOrInherit(e,t){let r=T.exec(t);return r&&(t=r[1]?this._getInitialValueForProperty(e):"apply-shim-inherit"),t}_cssTextToMap(e,t=!1){let r,n,s=e.split(";"),i={};for(let e,a,o=0;o<s.length;o++)e=s[o],e&&(a=e.split(":"),a.length>1&&(r=a[0].trim(),n=a.slice(1).join(":"),t&&(n=this._replaceInitialOrInherit(r,n)),i[r]=n));return i}_invalidateMixinEntry(e){if(R)for(let t in e.dependants)t!==this._currentElement&&R(t)}_produceCssProperties(e,t,r,n,s){if(r&&P(r,((e,t)=>{t&&this._map.get(t)&&(n=`@apply ${t};`)})),!n)return e;let i=this._consumeCssProperties(""+n,s),a=e.slice(0,e.indexOf("--")),o=this._cssTextToMap(i,!0),l=o,p=this._map.get(t),d=p&&p.properties;d?l=Object.assign(Object.create(d),o):this._map.set(t,l);let c,h,u=[],_=!1;for(c in l)h=o[c],void 0===h&&(h="initial"),d&&!(c in d)&&(_=!0),u.push(`${t}_-_${c}: ${h}`);return _&&this._invalidateMixinEntry(p),p&&(p.properties=l),r&&(a=`${e};${a}`),`${a}${u.join("; ")};`}}M.prototype.detectMixin=M.prototype.detectMixin,M.prototype.transformStyle=M.prototype.transformStyle,M.prototype.transformCustomStyle=M.prototype.transformCustomStyle,M.prototype.transformRules=M.prototype.transformRules,M.prototype.transformRule=M.prototype.transformRule,M.prototype.transformTemplate=M.prototype.transformTemplate,M.prototype._separator=I,Object.defineProperty(M.prototype,"invalidCallback",{get:()=>R,set(e){R=e}});const D=M,L={},F="_applyShimCurrentVersion",z="_applyShimNextVersion",j="_applyShimValidatingVersion",H=Promise.resolve();function B(e){let t=L[e];t&&function(e){e[F]=e[F]||0,e[j]=e[j]||0,e[z]=(e[z]||0)+1}(t)}function $(e){return e[F]===e[z]}function U(e){return!$(e)&&e[j]===e[z]}function J(e){e[j]=e[z],e._validating||(e._validating=!0,H.then((function(){e[F]=e[z],e._validating=!1})))}r(34816);const q=new D;class Y{constructor(){this.customStyleInterface=null,q.invalidCallback=B}ensure(){this.customStyleInterface||window.ShadyCSS.CustomStyleInterface&&(this.customStyleInterface=window.ShadyCSS.CustomStyleInterface,this.customStyleInterface.transformCallback=e=>{q.transformCustomStyle(e)},this.customStyleInterface.validateCallback=()=>{requestAnimationFrame((()=>{this.customStyleInterface.enqueued&&this.flushCustomStyles()}))})}prepareTemplate(e,t){if(this.ensure(),E(e))return;L[t]=e;let r=q.transformTemplate(e,t);e._styleAst=r}flushCustomStyles(){if(this.ensure(),!this.customStyleInterface)return;let e=this.customStyleInterface.processStyles();if(this.customStyleInterface.enqueued){for(let t=0;t<e.length;t++){let r=e[t],n=this.customStyleInterface.getStyleForCustomStyle(r);n&&q.transformCustomStyle(n)}this.customStyleInterface.enqueued=!1}}styleSubtree(e,t){if(this.ensure(),t&&(0,A.wW)(e,t),e.shadowRoot){this.styleElement(e);let t=e.shadowRoot.children||e.shadowRoot.childNodes;for(let e=0;e<t.length;e++)this.styleSubtree(t[e])}else{let t=e.children||e.childNodes;for(let e=0;e<t.length;e++)this.styleSubtree(t[e])}}styleElement(e){this.ensure();let{is:t}=function(e){let t=e.localName,r="",n="";return t?t.indexOf("-")>-1?r=t:(n=t,r=e.getAttribute&&e.getAttribute("is")||""):(r=e.is,n=e.extends),{is:r,typeExtension:n}}(e),r=L[t];if((!r||!E(r))&&r&&!$(r)){U(r)||(this.prepareTemplate(r,t),J(r));let n=e.shadowRoot;if(n){let e=n.querySelector("style");e&&(e.__cssRules=r._styleAst,e.textContent=b(r._styleAst))}}}styleDocument(e){this.ensure(),this.styleSubtree(document.body,e)}}if(!window.ShadyCSS||!window.ShadyCSS.ScopingShim){const e=new Y;let t=window.ShadyCSS&&window.ShadyCSS.CustomStyleInterface;window.ShadyCSS={prepareTemplate(t,r,n){e.flushCustomStyles(),e.prepareTemplate(t,r)},prepareTemplateStyles(e,t,r){window.ShadyCSS.prepareTemplate(e,t,r)},prepareTemplateDom(e,t){},styleSubtree(t,r){e.flushCustomStyles(),e.styleSubtree(t,r)},styleElement(t){e.flushCustomStyles(),e.styleElement(t)},styleDocument(t){e.flushCustomStyles(),e.styleDocument(t)},getComputedStyleValue:(e,t)=>(0,A.B7)(e,t),flushCustomStyles(){e.flushCustomStyles()},nativeCss:n.rd,nativeShadow:n.WA,cssBuild:n.Cp,disableRuntime:n.jF},t&&(window.ShadyCSS.CustomStyleInterface=t)}window.ShadyCSS.ApplyShim=q;var V=r(36608),W=r(60995),G=r(63933),Z=r(76389);const X=/:host\(:dir\((ltr|rtl)\)\)/g,K=/([\s\w-#\.\[\]\*]*):dir\((ltr|rtl)\)/g,Q=/:dir\((?:ltr|rtl)\)/,ee=Boolean(window.ShadyDOM&&window.ShadyDOM.inUse),te=[];let re=null,ne="";function se(){ne=document.documentElement.getAttribute("dir")}function ie(e){if(!e.__autoDirOptOut){e.setAttribute("dir",ne)}}function ae(){se(),ne=document.documentElement.getAttribute("dir");for(let e=0;e<te.length;e++)ie(te[e])}const oe=(0,Z.o)((e=>{ee||re||(se(),re=new MutationObserver(ae),re.observe(document.documentElement,{attributes:!0,attributeFilter:["dir"]}));const t=(0,G.Q)(e);class r extends t{static _processStyleText(e,r){return e=t._processStyleText.call(this,e,r),!ee&&Q.test(e)&&(e=this._replaceDirInCssText(e),this.__activateDir=!0),e}static _replaceDirInCssText(e){let t=e;return t=t.replace(X,':host([dir="$1"])'),t=t.replace(K,':host([dir="$2"]) $1'),t}constructor(){super(),this.__autoDirOptOut=!1}ready(){super.ready(),this.__autoDirOptOut=this.hasAttribute("dir")}connectedCallback(){t.prototype.connectedCallback&&super.connectedCallback(),this.constructor.__activateDir&&(re&&re.takeRecords().length&&ae(),te.push(this),ie(this))}disconnectedCallback(){if(t.prototype.disconnectedCallback&&super.disconnectedCallback(),this.constructor.__activateDir){const e=te.indexOf(this);e>-1&&te.splice(e,1)}}}return r.__activateDir=!1,r}));r(87529);function le(){document.body.removeAttribute("unresolved")}"interactive"===document.readyState||"complete"===document.readyState?le():window.addEventListener("DOMContentLoaded",le);var pe=r(87156),de=r(81668),ce=r(78956),he=r(21683),ue=r(4059),_e=r(62276);r(56646);const fe=window.ShadyDOM,me=window.ShadyCSS;function ye(e,t){return(0,_e.r)(e).getRootNode()===t}var ge=r(74460),be=r(16777),Ce=r(65412);const we="disable-upgrade";let xe=window.ShadyCSS;const Pe=(0,Z.o)((e=>{const t=(0,W._)((0,V.SH)(e)),r=V.PP?t:oe(t),n=(0,be.X)(r),s={x:"pan-x",y:"pan-y",none:"none",all:"auto"};class i extends r{constructor(){super(),this.isAttached,this.__boundListeners,this._debouncers,this.__isUpgradeDisabled,this.__needsAttributesAtConnected,this._legacyForceObservedAttributes}static get importMeta(){return this.prototype.importMeta}created(){}__attributeReaction(e,t,r){(this.__dataAttributes&&this.__dataAttributes[e]||e===we)&&this.attributeChangedCallback(e,t,r,null)}setAttribute(e,t){if(ge.j8&&!this._legacyForceObservedAttributes){const r=this.getAttribute(e);super.setAttribute(e,t),this.__attributeReaction(e,r,String(t))}else super.setAttribute(e,t)}removeAttribute(e){if(ge.j8&&!this._legacyForceObservedAttributes){const t=this.getAttribute(e);super.removeAttribute(e),this.__attributeReaction(e,t,null)}else super.removeAttribute(e)}static get observedAttributes(){return ge.j8&&!this.prototype._legacyForceObservedAttributes?(this.hasOwnProperty(JSCompiler_renameProperty("__observedAttributes",this))||(this.__observedAttributes=[],(0,Ce.z2)(this.prototype)),this.__observedAttributes):n.call(this).concat(we)}_enableProperties(){this.__isUpgradeDisabled||super._enableProperties()}_canApplyPropertyDefault(e){return super._canApplyPropertyDefault(e)&&!(this.__isUpgradeDisabled&&this._isPropertyPending(e))}connectedCallback(){this.__needsAttributesAtConnected&&this._takeAttributes(),this.__isUpgradeDisabled||(super.connectedCallback(),this.isAttached=!0,this.attached())}attached(){}disconnectedCallback(){this.__isUpgradeDisabled||(super.disconnectedCallback(),this.isAttached=!1,this.detached())}detached(){}attributeChangedCallback(e,t,r,n){t!==r&&(e==we?this.__isUpgradeDisabled&&null==r&&(this._initializeProperties(),this.__isUpgradeDisabled=!1,(0,_e.r)(this).isConnected&&this.connectedCallback()):(super.attributeChangedCallback(e,t,r,n),this.attributeChanged(e,t,r)))}attributeChanged(e,t,r){}_initializeProperties(){if(ge.nL&&this.hasAttribute(we))this.__isUpgradeDisabled=!0;else{let e=Object.getPrototypeOf(this);e.hasOwnProperty(JSCompiler_renameProperty("__hasRegisterFinished",e))||(this._registered(),e.__hasRegisterFinished=!0),super._initializeProperties(),this.root=this,this.created(),ge.j8&&!this._legacyForceObservedAttributes&&(this.hasAttributes()?this._takeAttributes():this.parentNode||(this.__needsAttributesAtConnected=!0)),this._applyListeners()}}_takeAttributes(){const e=this.attributes;for(let t=0,r=e.length;t<r;t++){const r=e[t];this.__attributeReaction(r.name,null,r.value)}}_registered(){}ready(){this._ensureAttributes(),super.ready()}_ensureAttributes(){}_applyListeners(){}serialize(e){return this._serializeValue(e)}deserialize(e,t){return this._deserializeValue(e,t)}reflectPropertyToAttribute(e,t,r){this._propertyToAttribute(e,t,r)}serializeValueToAttribute(e,t,r){this._valueToNodeAttribute(r||this,e,t)}extend(e,t){if(!e||!t)return e||t;let r=Object.getOwnPropertyNames(t);for(let n,s=0;s<r.length&&(n=r[s]);s++){let r=Object.getOwnPropertyDescriptor(t,n);r&&Object.defineProperty(e,n,r)}return e}mixin(e,t){for(let r in t)e[r]=t[r];return e}chainObject(e,t){return e&&t&&e!==t&&(e.__proto__=t),e}instanceTemplate(e){let t=this.constructor._contentForTemplate(e);return document.importNode(t,!0)}fire(e,t,r){r=r||{},t=null==t?{}:t;let n=new Event(e,{bubbles:void 0===r.bubbles||r.bubbles,cancelable:Boolean(r.cancelable),composed:void 0===r.composed||r.composed});n.detail=t;let s=r.node||this;return(0,_e.r)(s).dispatchEvent(n),n}listen(e,t,r){e=e||this;let n=this.__boundListeners||(this.__boundListeners=new WeakMap),s=n.get(e);s||(s={},n.set(e,s));let i=t+r;s[i]||(s[i]=this._addMethodEventListenerToNode(e,t,r,this))}unlisten(e,t,r){e=e||this;let n=this.__boundListeners&&this.__boundListeners.get(e),s=t+r,i=n&&n[s];i&&(this._removeEventListenerFromNode(e,t,i),n[s]=null)}setScrollDirection(e,t){(0,de.BP)(t||this,s[e]||"auto")}$$(e){return this.root.querySelector(e)}get domHost(){let e=(0,_e.r)(this).getRootNode();return e instanceof DocumentFragment?e.host:e}distributeContent(){const e=(0,pe.vz)(this);window.ShadyDOM&&e.shadowRoot&&ShadyDOM.flush()}getEffectiveChildNodes(){return(0,pe.vz)(this).getEffectiveChildNodes()}queryDistributedElements(e){return(0,pe.vz)(this).queryDistributedElements(e)}getEffectiveChildren(){return this.getEffectiveChildNodes().filter((function(e){return e.nodeType===Node.ELEMENT_NODE}))}getEffectiveTextContent(){let e=this.getEffectiveChildNodes(),t=[];for(let r,n=0;r=e[n];n++)r.nodeType!==Node.COMMENT_NODE&&t.push(r.textContent);return t.join("")}queryEffectiveChildren(e){let t=this.queryDistributedElements(e);return t&&t[0]}queryAllEffectiveChildren(e){return this.queryDistributedElements(e)}getContentChildNodes(e){let t=this.root.querySelector(e||"slot");return t?(0,pe.vz)(t).getDistributedNodes():[]}getContentChildren(e){return this.getContentChildNodes(e).filter((function(e){return e.nodeType===Node.ELEMENT_NODE}))}isLightDescendant(e){const t=this;return t!==e&&(0,_e.r)(t).contains(e)&&(0,_e.r)(t).getRootNode()===(0,_e.r)(e).getRootNode()}isLocalDescendant(e){return this.root===(0,_e.r)(e).getRootNode()}scopeSubtree(e,t=!1){return function(e,t=!1){if(!fe||!me)return null;if(!fe.handlesDynamicScoping)return null;const r=me.ScopingShim;if(!r)return null;const n=r.scopeForNode(e),s=(0,_e.r)(e).getRootNode(),i=e=>{if(!ye(e,s))return;const t=Array.from(fe.nativeMethods.querySelectorAll.call(e,"*"));t.push(e);for(let e=0;e<t.length;e++){const i=t[e];if(!ye(i,s))continue;const a=r.currentScopeForNode(i);a!==n&&(""!==a&&r.unscopeNode(i,a),r.scopeNode(i,n))}};if(i(e),t){const t=new MutationObserver((e=>{for(let t=0;t<e.length;t++){const r=e[t];for(let e=0;e<r.addedNodes.length;e++){const t=r.addedNodes[e];t.nodeType===Node.ELEMENT_NODE&&i(t)}}}));return t.observe(e,{childList:!0,subtree:!0}),t}return null}(e,t)}getComputedStyleValue(e){return xe.getComputedStyleValue(this,e)}debounce(e,t,r){return this._debouncers=this._debouncers||{},this._debouncers[e]=ce.dx.debounce(this._debouncers[e],r>0?he.Wc.after(r):he.YA,t.bind(this))}isDebouncerActive(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];return!(!t||!t.isActive())}flushDebouncer(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];t&&t.flush()}cancelDebouncer(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];t&&t.cancel()}async(e,t){return t>0?he.Wc.run(e.bind(this),t):~he.YA.run(e.bind(this))}cancelAsync(e){e<0?he.YA.cancel(~e):he.Wc.cancel(e)}create(e,t){let r=document.createElement(e);if(t)if(r.setProperties)r.setProperties(t);else for(let e in t)r[e]=t[e];return r}elementMatches(e,t){return(0,pe.Ku)(t||this,e)}toggleAttribute(e,t){let r=this;return 3===arguments.length&&(r=arguments[2]),1==arguments.length&&(t=!r.hasAttribute(e)),t?((0,_e.r)(r).setAttribute(e,""),!0):((0,_e.r)(r).removeAttribute(e),!1)}toggleClass(e,t,r){r=r||this,1==arguments.length&&(t=!r.classList.contains(e)),t?r.classList.add(e):r.classList.remove(e)}transform(e,t){(t=t||this).style.webkitTransform=e,t.style.transform=e}translate3d(e,t,r,n){n=n||this,this.transform("translate3d("+e+","+t+","+r+")",n)}arrayDelete(e,t){let r;if(Array.isArray(e)){if(r=e.indexOf(t),r>=0)return e.splice(r,1)}else{if(r=(0,ue.U2)(this,e).indexOf(t),r>=0)return this.splice(e,r,1)}return null}_logger(e,t){switch(Array.isArray(t)&&1===t.length&&Array.isArray(t[0])&&(t=t[0]),e){case"log":case"warn":case"error":console[e](...t)}}_log(...e){this._logger("log",e)}_warn(...e){this._logger("warn",e)}_error(...e){this._logger("error",e)}_logf(e,...t){return["[%s::%s]",this.is,e,...t]}}return i.prototype.is="",i}))},36608:(e,t,r)=>{r.d(t,{SH:()=>_,PP:()=>u});r(56646);var n=r(74460),s=r(76389),i=r(15392),a=r(42687),o=r(21384),l=r(40729),p=r(65412),d=r(24072);const c=(0,s.o)((e=>{const t=(0,d.e)(e);function r(e){const t=Object.getPrototypeOf(e);return t.prototype instanceof s?t:null}function n(e){if(!e.hasOwnProperty(JSCompiler_renameProperty("__ownProperties",e))){let t=null;if(e.hasOwnProperty(JSCompiler_renameProperty("properties",e))){const r=e.properties;r&&(t=function(e){const t={};for(let r in e){const n=e[r];t[r]="function"==typeof n?{type:n}:n}return t}(r))}e.__ownProperties=t}return e.__ownProperties}class s extends t{static get observedAttributes(){if(!this.hasOwnProperty(JSCompiler_renameProperty("__observedAttributes",this))){(0,p.z2)(this.prototype);const e=this._properties;this.__observedAttributes=e?Object.keys(e).map((e=>this.prototype._addPropertyToAttributeMap(e))):[]}return this.__observedAttributes}static finalize(){if(!this.hasOwnProperty(JSCompiler_renameProperty("__finalized",this))){const e=r(this);e&&e.finalize(),this.__finalized=!0,this._finalizeClass()}}static _finalizeClass(){const e=n(this);e&&this.createProperties(e)}static get _properties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("__properties",this))){const e=r(this);this.__properties=Object.assign({},e&&e._properties,n(this))}return this.__properties}static typeForProperty(e){const t=this._properties[e];return t&&t.type}_initializeProperties(){(0,p.Gd)(),this.constructor.finalize(),super._initializeProperties()}connectedCallback(){super.connectedCallback&&super.connectedCallback(),this._enableProperties()}disconnectedCallback(){super.disconnectedCallback&&super.disconnectedCallback()}}return s}));var h=r(62276);const u=window.ShadyCSS&&window.ShadyCSS.cssBuild,_=(0,s.o)((e=>{const t=c((0,l.q)(e));return class extends t{static get polymerElementVersion(){return"3.4.1"}static _finalizeClass(){t._finalizeClass.call(this);const e=((r=this).hasOwnProperty(JSCompiler_renameProperty("__ownObservers",r))||(r.__ownObservers=r.hasOwnProperty(JSCompiler_renameProperty("observers",r))?r.observers:null),r.__ownObservers);var r;e&&this.createObservers(e,this._properties),this._prepareTemplate()}static _prepareTemplate(){let e=this.template;e&&("string"==typeof e?(console.error("template getter must return HTMLTemplateElement"),e=null):n.nL||(e=e.cloneNode(!0))),this.prototype._template=e}static createProperties(e){for(let i in e)t=this.prototype,r=i,n=e[i],s=e,n.computed&&(n.readOnly=!0),n.computed&&(t._hasReadOnlyEffect(r)?console.warn(`Cannot redefine computed property '${r}'.`):t._createComputedProperty(r,n.computed,s)),n.readOnly&&!t._hasReadOnlyEffect(r)?t._createReadOnlyProperty(r,!n.computed):!1===n.readOnly&&t._hasReadOnlyEffect(r)&&console.warn(`Cannot make readOnly property '${r}' non-readOnly.`),n.reflectToAttribute&&!t._hasReflectEffect(r)?t._createReflectedProperty(r):!1===n.reflectToAttribute&&t._hasReflectEffect(r)&&console.warn(`Cannot make reflected property '${r}' non-reflected.`),n.notify&&!t._hasNotifyEffect(r)?t._createNotifyingProperty(r):!1===n.notify&&t._hasNotifyEffect(r)&&console.warn(`Cannot make notify property '${r}' non-notify.`),n.observer&&t._createPropertyObserver(r,n.observer,s[n.observer]),t._addPropertyToAttributeMap(r);var t,r,n,s}static createObservers(e,t){const r=this.prototype;for(let n=0;n<e.length;n++)r._createMethodObserver(e[n],t)}static get template(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_template",this))){const e=this.prototype.hasOwnProperty(JSCompiler_renameProperty("_template",this.prototype))?this.prototype._template:void 0;this._template=void 0!==e?e:this.hasOwnProperty(JSCompiler_renameProperty("is",this))&&function(e){let t=null;if(e&&(!n.XN||n.ZN)&&(t=o.t.import(e,"template"),n.XN&&!t))throw new Error(`strictTemplatePolicy: expecting dom-module or null template for ${e}`);return t}(this.is)||Object.getPrototypeOf(this.prototype).constructor.template}return this._template}static set template(e){this._template=e}static get importPath(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_importPath",this))){const e=this.importMeta;if(e)this._importPath=(0,a.iY)(e.url);else{const e=o.t.import(this.is);this._importPath=e&&e.assetpath||Object.getPrototypeOf(this.prototype).constructor.importPath}}return this._importPath}constructor(){super(),this._template,this._importPath,this.rootPath,this.importPath,this.root,this.$}_initializeProperties(){this.constructor.finalize(),this.constructor._finalizeTemplate(this.localName),super._initializeProperties(),this.rootPath=n.sM,this.importPath=this.constructor.importPath;let e=function(e){if(!e.hasOwnProperty(JSCompiler_renameProperty("__propertyDefaults",e))){e.__propertyDefaults=null;let t=e._properties;for(let r in t){let n=t[r];"value"in n&&(e.__propertyDefaults=e.__propertyDefaults||{},e.__propertyDefaults[r]=n)}}return e.__propertyDefaults}(this.constructor);if(e)for(let t in e){let r=e[t];if(this._canApplyPropertyDefault(t)){let e="function"==typeof r.value?r.value.call(this):r.value;this._hasAccessor(t)?this._setPendingProperty(t,e,!0):this[t]=e}}}_canApplyPropertyDefault(e){return!this.hasOwnProperty(e)}static _processStyleText(e,t){return(0,a.Rq)(e,t)}static _finalizeTemplate(e){const t=this.prototype._template;if(t&&!t.__polymerFinalized){t.__polymerFinalized=!0;const r=this.importPath;!function(e,t,r,s){if(!u){const n=t.content.querySelectorAll("style"),a=(0,i.uT)(t),o=(0,i.lx)(r),l=t.content.firstElementChild;for(let r=0;r<o.length;r++){let n=o[r];n.textContent=e._processStyleText(n.textContent,s),t.content.insertBefore(n,l)}let p=0;for(let t=0;t<a.length;t++){let r=a[t],i=n[p];i!==r?(r=r.cloneNode(!0),i.parentNode.insertBefore(r,i)):p++,r.textContent=e._processStyleText(r.textContent,s)}}if(window.ShadyCSS&&window.ShadyCSS.prepareTemplate(t,r),n.md&&u&&n.FV){const r=t.content.querySelectorAll("style");if(r){let t="";Array.from(r).forEach((e=>{t+=e.textContent,e.parentNode.removeChild(e)})),e._styleSheet=new CSSStyleSheet,e._styleSheet.replaceSync(t)}}}(this,t,e,r?(0,a.Kk)(r):""),this.prototype._bindTemplate(t)}}connectedCallback(){window.ShadyCSS&&this._template&&window.ShadyCSS.styleElement(this),super.connectedCallback()}ready(){this._template&&(this.root=this._stampTemplate(this._template),this.$=this.root.$),super.ready()}_readyClients(){this._template&&(this.root=this._attachDom(this.root)),super._readyClients()}_attachDom(e){const t=(0,h.r)(this);if(t.attachShadow)return e?(t.shadowRoot||(t.attachShadow({mode:"open",shadyUpgradeFragment:e}),t.shadowRoot.appendChild(e),this.constructor._styleSheet&&(t.shadowRoot.adoptedStyleSheets=[this.constructor._styleSheet])),n.Hr&&window.ShadyDOM&&window.ShadyDOM.flushInitial(t.shadowRoot),t.shadowRoot):null;throw new Error("ShadowDOM not available. PolymerElement can create dom as children instead of in ShadowDOM by setting `this.root = this;` before `ready`.")}updateStyles(e){window.ShadyCSS&&window.ShadyCSS.styleSubtree(this,e)}resolveUrl(e,t){return!t&&this.importPath&&(t=(0,a.Kk)(this.importPath)),(0,a.Kk)(e,t)}static _parseTemplateContent(e,r,n){return r.dynamicFns=r.dynamicFns||this._properties,t._parseTemplateContent.call(this,e,r,n)}static _addTemplatePropertyEffect(e,r,s){return!n.a2||r in this._properties||s.info.part.signature&&s.info.part.signature.static||s.info.part.hostProp||e.nestedTemplate||console.warn(`Property '${r}' used in template but not declared in 'properties'; attribute will not be observed.`),t._addTemplatePropertyEffect.call(this,e,r,s)}}}))},60995:(e,t,r)=>{r.d(t,{_:()=>i});r(56646);var n=r(76389),s=r(81668);const i=(0,n.o)((e=>class extends e{_addEventListenerToNode(e,t,r){(0,s.NH)(e,t,r)||super._addEventListenerToNode(e,t,r)}_removeEventListenerFromNode(e,t,r){(0,s.ys)(e,t,r)||super._removeEventListenerFromNode(e,t,r)}}))},18691:(e,t,r)=>{r.d(t,{E:()=>i,w:()=>a});var n=r(76389);function s(e,t,r,n,s){let i;s&&(i="object"==typeof r&&null!==r,i&&(n=e.__dataTemp[t]));let a=n!==r&&(n==n||r==r);return i&&a&&(e.__dataTemp[t]=r),a}const i=(0,n.o)((e=>class extends e{_shouldPropertyChange(e,t,r){return s(this,e,t,r,!0)}})),a=(0,n.o)((e=>class extends e{static get properties(){return{mutableData:Boolean}}_shouldPropertyChange(e,t,r){return s(this,e,t,r,this.mutableData)}}));i._mutablePropertyChange=s},24072:(e,t,r)=>{r.d(t,{e:()=>o});r(56646);var n=r(76389),s=r(21683),i=r(62276);const a=s.YA,o=(0,n.o)((e=>class extends e{static createProperties(e){const t=this.prototype;for(let r in e)r in t||t._createPropertyAccessor(r)}static attributeNameForProperty(e){return e.toLowerCase()}static typeForProperty(e){}_createPropertyAccessor(e,t){this._addPropertyToAttributeMap(e),this.hasOwnProperty(JSCompiler_renameProperty("__dataHasAccessor",this))||(this.__dataHasAccessor=Object.assign({},this.__dataHasAccessor)),this.__dataHasAccessor[e]||(this.__dataHasAccessor[e]=!0,this._definePropertyAccessor(e,t))}_addPropertyToAttributeMap(e){this.hasOwnProperty(JSCompiler_renameProperty("__dataAttributes",this))||(this.__dataAttributes=Object.assign({},this.__dataAttributes));let t=this.__dataAttributes[e];return t||(t=this.constructor.attributeNameForProperty(e),this.__dataAttributes[t]=e),t}_definePropertyAccessor(e,t){Object.defineProperty(this,e,{get(){return this.__data[e]},set:t?function(){}:function(t){this._setPendingProperty(e,t,!0)&&this._invalidateProperties()}})}constructor(){super(),this.__dataEnabled=!1,this.__dataReady=!1,this.__dataInvalid=!1,this.__data={},this.__dataPending=null,this.__dataOld=null,this.__dataInstanceProps=null,this.__dataCounter=0,this.__serializing=!1,this._initializeProperties()}ready(){this.__dataReady=!0,this._flushProperties()}_initializeProperties(){for(let e in this.__dataHasAccessor)this.hasOwnProperty(e)&&(this.__dataInstanceProps=this.__dataInstanceProps||{},this.__dataInstanceProps[e]=this[e],delete this[e])}_initializeInstanceProperties(e){Object.assign(this,e)}_setProperty(e,t){this._setPendingProperty(e,t)&&this._invalidateProperties()}_getProperty(e){return this.__data[e]}_setPendingProperty(e,t,r){let n=this.__data[e],s=this._shouldPropertyChange(e,t,n);return s&&(this.__dataPending||(this.__dataPending={},this.__dataOld={}),this.__dataOld&&!(e in this.__dataOld)&&(this.__dataOld[e]=n),this.__data[e]=t,this.__dataPending[e]=t),s}_isPropertyPending(e){return!(!this.__dataPending||!this.__dataPending.hasOwnProperty(e))}_invalidateProperties(){!this.__dataInvalid&&this.__dataReady&&(this.__dataInvalid=!0,a.run((()=>{this.__dataInvalid&&(this.__dataInvalid=!1,this._flushProperties())})))}_enableProperties(){this.__dataEnabled||(this.__dataEnabled=!0,this.__dataInstanceProps&&(this._initializeInstanceProperties(this.__dataInstanceProps),this.__dataInstanceProps=null),this.ready())}_flushProperties(){this.__dataCounter++;const e=this.__data,t=this.__dataPending,r=this.__dataOld;this._shouldPropertiesChange(e,t,r)&&(this.__dataPending=null,this.__dataOld=null,this._propertiesChanged(e,t,r)),this.__dataCounter--}_shouldPropertiesChange(e,t,r){return Boolean(t)}_propertiesChanged(e,t,r){}_shouldPropertyChange(e,t,r){return r!==t&&(r==r||t==t)}attributeChangedCallback(e,t,r,n){t!==r&&this._attributeToProperty(e,r),super.attributeChangedCallback&&super.attributeChangedCallback(e,t,r,n)}_attributeToProperty(e,t,r){if(!this.__serializing){const n=this.__dataAttributes,s=n&&n[e]||e;this[s]=this._deserializeValue(t,r||this.constructor.typeForProperty(s))}}_propertyToAttribute(e,t,r){this.__serializing=!0,r=arguments.length<3?this[e]:r,this._valueToNodeAttribute(this,r,t||this.constructor.attributeNameForProperty(e)),this.__serializing=!1}_valueToNodeAttribute(e,t,r){const n=this._serializeValue(t);"class"!==r&&"name"!==r&&"slot"!==r||(e=(0,i.r)(e)),void 0===n?e.removeAttribute(r):e.setAttribute(r,n)}_serializeValue(e){return"boolean"==typeof e?e?"":void 0:null!=e?e.toString():void 0}_deserializeValue(e,t){switch(t){case Boolean:return null!==e;case Number:return Number(e);default:return e}}}))},63933:(e,t,r)=>{r.d(t,{Q:()=>l});r(56646);var n=r(76389),s=r(67130),i=r(24072);const a={};let o=HTMLElement.prototype;for(;o;){let e=Object.getOwnPropertyNames(o);for(let t=0;t<e.length;t++)a[e[t]]=!0;o=Object.getPrototypeOf(o)}const l=(0,n.o)((e=>{const t=(0,i.e)(e);return class extends t{static createPropertiesForAttributes(){let e=this.observedAttributes;for(let t=0;t<e.length;t++)this.prototype._createPropertyAccessor((0,s.z)(e[t]))}static attributeNameForProperty(e){return(0,s.n)(e)}_initializeProperties(){this.__dataProto&&(this._initializeProtoProperties(this.__dataProto),this.__dataProto=null),super._initializeProperties()}_initializeProtoProperties(e){for(let t in e)this._setProperty(t,e[t])}_ensureAttribute(e,t){const r=this;r.hasAttribute(e)||this._valueToNodeAttribute(r,t,e)}_serializeValue(e){if("object"==typeof e){if(e instanceof Date)return e.toString();if(e)try{return JSON.stringify(e)}catch(e){return""}}return super._serializeValue(e)}_deserializeValue(e,t){let r;switch(t){case Object:try{r=JSON.parse(e)}catch(t){r=e}break;case Array:try{r=JSON.parse(e)}catch(t){r=null,console.warn(`Polymer::Attributes: couldn't decode Array as JSON: ${e}`)}break;case Date:r=isNaN(e)?String(e):Number(e),r=new Date(r);break;default:r=super._deserializeValue(e,t)}return r}_definePropertyAccessor(e,t){!function(e,t){if(!a[t]){let r=e[t];void 0!==r&&(e.__data?e._setPendingProperty(t,r):(e.__dataProto?e.hasOwnProperty(JSCompiler_renameProperty("__dataProto",e))||(e.__dataProto=Object.create(e.__dataProto)):e.__dataProto={},e.__dataProto[t]=r))}}(this,e),super._definePropertyAccessor(e,t)}_hasAccessor(e){return this.__dataHasAccessor&&this.__dataHasAccessor[e]}_isPropertyPending(e){return Boolean(this.__dataPending&&e in this.__dataPending)}}}))},40729:(e,t,r)=>{r.d(t,{q:()=>K});r(56646);var n=r(62276),s=r(76389),i=r(4059),a=r(67130),o=r(63933);const l={"dom-if":!0,"dom-repeat":!0};let p=!1,d=!1;function c(e){(function(){if(!p){p=!0;const e=document.createElement("textarea");e.placeholder="a",d=e.placeholder===e.textContent}return d})()&&"textarea"===e.localName&&e.placeholder&&e.placeholder===e.textContent&&(e.textContent=null)}function h(e){let t=e.getAttribute("is");if(t&&l[t]){let r=e;for(r.removeAttribute("is"),e=r.ownerDocument.createElement(t),r.parentNode.replaceChild(e,r),e.appendChild(r);r.attributes.length;)e.setAttribute(r.attributes[0].name,r.attributes[0].value),r.removeAttribute(r.attributes[0].name)}return e}function u(e,t){let r=t.parentInfo&&u(e,t.parentInfo);if(!r)return e;for(let e=r.firstChild,n=0;e;e=e.nextSibling)if(t.parentIndex===n++)return e}function _(e,t,r,n){n.id&&(t[n.id]=r)}function f(e,t,r){if(r.events&&r.events.length)for(let n,s=0,i=r.events;s<i.length&&(n=i[s]);s++)e._addMethodEventListenerToNode(t,n.name,n.value,e)}function m(e,t,r,n){r.templateInfo&&(t._templateInfo=r.templateInfo,t._parentTemplateInfo=n)}const y=(0,s.o)((e=>class extends e{static _parseTemplate(e,t){if(!e._templateInfo){let r=e._templateInfo={};r.nodeInfoList=[],r.nestedTemplate=Boolean(t),r.stripWhiteSpace=t&&t.stripWhiteSpace||e.hasAttribute("strip-whitespace"),this._parseTemplateContent(e,r,{parent:null})}return e._templateInfo}static _parseTemplateContent(e,t,r){return this._parseTemplateNode(e.content,t,r)}static _parseTemplateNode(e,t,r){let n=!1,s=e;return"template"!=s.localName||s.hasAttribute("preserve-content")?"slot"===s.localName&&(t.hasInsertionPoint=!0):n=this._parseTemplateNestedTemplate(s,t,r)||n,c(s),s.firstChild&&this._parseTemplateChildNodes(s,t,r),s.hasAttributes&&s.hasAttributes()&&(n=this._parseTemplateNodeAttributes(s,t,r)||n),n||r.noted}static _parseTemplateChildNodes(e,t,r){if("script"!==e.localName&&"style"!==e.localName)for(let n,s=e.firstChild,i=0;s;s=n){if("template"==s.localName&&(s=h(s)),n=s.nextSibling,s.nodeType===Node.TEXT_NODE){let r=n;for(;r&&r.nodeType===Node.TEXT_NODE;)s.textContent+=r.textContent,n=r.nextSibling,e.removeChild(r),r=n;if(t.stripWhiteSpace&&!s.textContent.trim()){e.removeChild(s);continue}}let a={parentIndex:i,parentInfo:r};this._parseTemplateNode(s,t,a)&&(a.infoIndex=t.nodeInfoList.push(a)-1),s.parentNode&&i++}}static _parseTemplateNestedTemplate(e,t,r){let n=e,s=this._parseTemplate(n,t);return(s.content=n.content.ownerDocument.createDocumentFragment()).appendChild(n.content),r.templateInfo=s,!0}static _parseTemplateNodeAttributes(e,t,r){let n=!1,s=Array.from(e.attributes);for(let i,a=s.length-1;i=s[a];a--)n=this._parseTemplateNodeAttribute(e,t,r,i.name,i.value)||n;return n}static _parseTemplateNodeAttribute(e,t,r,n,s){return"on-"===n.slice(0,3)?(e.removeAttribute(n),r.events=r.events||[],r.events.push({name:n.slice(3),value:s}),!0):"id"===n&&(r.id=s,!0)}static _contentForTemplate(e){let t=e._templateInfo;return t&&t.content||e.content}_stampTemplate(e,t){e&&!e.content&&window.HTMLTemplateElement&&HTMLTemplateElement.decorate&&HTMLTemplateElement.decorate(e);let r=(t=t||this.constructor._parseTemplate(e)).nodeInfoList,n=t.content||e.content,s=document.importNode(n,!0);s.__noInsertionPoint=!t.hasInsertionPoint;let i=s.nodeList=new Array(r.length);s.$={};for(let e,n=0,a=r.length;n<a&&(e=r[n]);n++){let r=i[n]=u(s,e);_(0,s.$,r,e),m(0,r,e,t),f(this,r,e)}return s=s,s}_addMethodEventListenerToNode(e,t,r,n){let s=function(e,t,r){return e=e._methodHost||e,function(t){e[r]?e[r](t,t.detail):console.warn("listener method `"+r+"` not defined")}}(n=n||e,0,r);return this._addEventListenerToNode(e,t,s),s}_addEventListenerToNode(e,t,r){e.addEventListener(t,r)}_removeEventListenerFromNode(e,t,r){e.removeEventListener(t,r)}}));var g=r(74460);let b=0;const C=[],w={COMPUTE:"__computeEffects",REFLECT:"__reflectEffects",NOTIFY:"__notifyEffects",PROPAGATE:"__propagateEffects",OBSERVE:"__observeEffects",READ_ONLY:"__readOnly"},x="__computeInfo",P=/[A-Z]/;function S(e,t,r){let n=e[t];if(n){if(!e.hasOwnProperty(t)&&(n=e[t]=Object.create(e[t]),r))for(let e in n){let t=n[e],r=n[e]=Array(t.length);for(let e=0;e<t.length;e++)r[e]=t[e]}}else n=e[t]={};return n}function v(e,t,r,n,s,a){if(t){let o=!1;const l=b++;for(let p in r){let d=t[s?(0,i.Jz)(p):p];if(d)for(let t,i=0,c=d.length;i<c&&(t=d[i]);i++)t.info&&t.info.lastRun===l||s&&!A(p,t.trigger)||(t.info&&(t.info.lastRun=l),t.fn(e,p,r,n,t.info,s,a),o=!0)}return o}return!1}function E(e,t,r,n,s,a,o,l){let p=!1,d=t[o?(0,i.Jz)(n):n];if(d)for(let t,i=0,c=d.length;i<c&&(t=d[i]);i++)t.info&&t.info.lastRun===r||o&&!A(n,t.trigger)||(t.info&&(t.info.lastRun=r),t.fn(e,n,s,a,t.info,o,l),p=!0);return p}function A(e,t){if(t){let r=t.name;return r==e||!(!t.structured||!(0,i.jg)(r,e))||!(!t.wildcard||!(0,i.SG)(r,e))}return!0}function O(e,t,r,n,s){let i="string"==typeof s.method?e[s.method]:s.method,a=s.property;i?i.call(e,e.__data[a],n[a]):s.dynamicFn||console.warn("observer method `"+s.method+"` not defined")}function T(e,t,r){let n=(0,i.Jz)(t);if(n!==t){return k(e,(0,a.n)(n)+"-changed",r[t],t),!0}return!1}function k(e,t,r,s){let i={value:r,queueProperty:!0};s&&(i.path=s),(0,n.r)(e).dispatchEvent(new CustomEvent(t,{detail:i}))}function I(e,t,r,n,s,a){let o=(a?(0,i.Jz)(t):t)!=t?t:null,l=o?(0,i.U2)(e,o):e.__data[t];o&&void 0===l&&(l=r[t]),k(e,s.eventName,l,o)}function N(e,t,r,n,s){let i=e.__data[t];g.v1&&(i=(0,g.v1)(i,s.attrName,"attribute",e)),e._propertyToAttribute(t,s.attrName,i)}function R(e,t,r,n){let s=e[w.COMPUTE];if(s)if(g.ls){b++;const i=function(e){let t=e.constructor.__orderedComputedDeps;if(!t){t=new Map;const r=e[w.COMPUTE];let n,{counts:s,ready:i,total:a}=function(e){const t=e.__computeInfo,r={},n=e[w.COMPUTE],s=[];let i=0;for(let e in t){const n=t[e];i+=r[e]=n.args.filter((e=>!e.literal)).length+(n.dynamicFn?1:0)}for(let e in n)t[e]||s.push(e);return{counts:r,ready:s,total:i}}(e);for(;n=i.shift();){t.set(n,t.size);const e=r[n];e&&e.forEach((e=>{const t=e.info.methodInfo;--a,0==--s[t]&&i.push(t)}))}if(0!==a){const t=e;console.warn(`Computed graph for ${t.localName} incomplete; circular?`)}e.constructor.__orderedComputedDeps=t}return t}(e),a=[];for(let e in t)D(e,s,a,i,n);let o;for(;o=a.shift();)L(e,"",t,r,o)&&D(o.methodInfo,s,a,i,n);Object.assign(r,e.__dataOld),Object.assign(t,e.__dataPending),e.__dataPending=null}else{let i=t;for(;v(e,s,i,r,n);)Object.assign(r,e.__dataOld),Object.assign(t,e.__dataPending),i=e.__dataPending,e.__dataPending=null}}const M=(e,t,r)=>{let n=0,s=t.length-1,i=-1;for(;n<=s;){const a=n+s>>1,o=r.get(t[a].methodInfo)-r.get(e.methodInfo);if(o<0)n=a+1;else{if(!(o>0)){i=a;break}s=a-1}}i<0&&(i=s+1),t.splice(i,0,e)},D=(e,t,r,n,s)=>{const a=t[s?(0,i.Jz)(e):e];if(a)for(let t=0;t<a.length;t++){const i=a[t];i.info.lastRun===b||s&&!A(e,i.trigger)||(i.info.lastRun=b,M(i.info,r,n))}};function L(e,t,r,n,s){let i=U(e,t,r,n,s);if(i===C)return!1;let a=s.methodInfo;return e.__dataHasAccessor&&e.__dataHasAccessor[a]?e._setPendingProperty(a,i,!0):(e[a]=i,!1)}function F(e,t,r,n,s,i,o){r.bindings=r.bindings||[];let l={kind:n,target:s,parts:i,literal:o,isCompound:1!==i.length};if(r.bindings.push(l),function(e){return Boolean(e.target)&&"attribute"!=e.kind&&"text"!=e.kind&&!e.isCompound&&"{"===e.parts[0].mode}(l)){let{event:e,negate:t}=l.parts[0];l.listenerEvent=e||(0,a.n)(s)+"-changed",l.listenerNegate=t}let p=t.nodeInfoList.length;for(let r=0;r<l.parts.length;r++){let n=l.parts[r];n.compoundIndex=r,z(e,t,l,n,p)}}function z(e,t,r,n,s){if(!n.literal)if("attribute"===r.kind&&"-"===r.target[0])console.warn("Cannot set attribute "+r.target+' because "-" is not a valid attribute starting character');else{let i=n.dependencies,a={index:s,binding:r,part:n,evaluator:e};for(let r=0;r<i.length;r++){let n=i[r];"string"==typeof n&&(n=W(n),n.wildcard=!0),e._addTemplatePropertyEffect(t,n.rootProperty,{fn:j,info:a,trigger:n})}}}function j(e,t,r,n,s,a,o){let l=o[s.index],p=s.binding,d=s.part;if(a&&d.source&&t.length>d.source.length&&"property"==p.kind&&!p.isCompound&&l.__isPropertyEffectsClient&&l.__dataHasAccessor&&l.__dataHasAccessor[p.target]){let n=r[t];t=(0,i.Iu)(d.source,p.target,t),l._setPendingPropertyOrPath(t,n,!1,!0)&&e._enqueueClient(l)}else{let i=s.evaluator._evaluateBinding(e,d,t,r,n,a);i!==C&&function(e,t,r,n,s){s=function(e,t,r,n){if(r.isCompound){let s=e.__dataCompoundStorage[r.target];s[n.compoundIndex]=t,t=s.join("")}"attribute"!==r.kind&&("textContent"!==r.target&&("value"!==r.target||"input"!==e.localName&&"textarea"!==e.localName)||(t=null==t?"":t));return t}(t,s,r,n),g.v1&&(s=(0,g.v1)(s,r.target,r.kind,t));if("attribute"==r.kind)e._valueToNodeAttribute(t,s,r.target);else{let n=r.target;t.__isPropertyEffectsClient&&t.__dataHasAccessor&&t.__dataHasAccessor[n]?t[w.READ_ONLY]&&t[w.READ_ONLY][n]||t._setPendingProperty(n,s)&&e._enqueueClient(t):e._setUnmanagedPropertyToNode(t,n,s)}}(e,l,p,d,i)}}function H(e,t){if(t.isCompound){let r=e.__dataCompoundStorage||(e.__dataCompoundStorage={}),s=t.parts,i=new Array(s.length);for(let e=0;e<s.length;e++)i[e]=s[e].literal;let a=t.target;r[a]=i,t.literal&&"property"==t.kind&&("className"===a&&(e=(0,n.r)(e)),e[a]=t.literal)}}function B(e,t,r){if(r.listenerEvent){let n=r.parts[0];e.addEventListener(r.listenerEvent,(function(e){!function(e,t,r,n,s){let a,o=e.detail,l=o&&o.path;l?(n=(0,i.Iu)(r,n,l),a=o&&o.value):a=e.currentTarget[r],a=s?!a:a,t[w.READ_ONLY]&&t[w.READ_ONLY][n]||!t._setPendingPropertyOrPath(n,a,!0,Boolean(l))||o&&o.queueProperty||t._invalidateProperties()}(e,t,r.target,n.source,n.negate)}))}}function $(e,t,r,n,s,i){i=t.static||i&&("object"!=typeof i||i[t.methodName]);let a={methodName:t.methodName,args:t.args,methodInfo:s,dynamicFn:i};for(let s,i=0;i<t.args.length&&(s=t.args[i]);i++)s.literal||e._addPropertyEffect(s.rootProperty,r,{fn:n,info:a,trigger:s});return i&&e._addPropertyEffect(t.methodName,r,{fn:n,info:a}),a}function U(e,t,r,n,s){let i=e._methodHost||e,a=i[s.methodName];if(a){let n=e._marshalArgs(s.args,t,r);return n===C?C:a.apply(i,n)}s.dynamicFn||console.warn("method `"+s.methodName+"` not defined")}const J=[],q=new RegExp("(\\[\\[|{{)\\s*(?:(!)\\s*)?((?:[a-zA-Z_$][\\w.:$\\-*]*)\\s*(?:\\(\\s*(?:(?:(?:((?:[a-zA-Z_$][\\w.:$\\-*]*)|(?:[-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?)|(?:(?:'(?:[^'\\\\]|\\\\.)*')|(?:\"(?:[^\"\\\\]|\\\\.)*\")))\\s*)(?:,\\s*(?:((?:[a-zA-Z_$][\\w.:$\\-*]*)|(?:[-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?)|(?:(?:'(?:[^'\\\\]|\\\\.)*')|(?:\"(?:[^\"\\\\]|\\\\.)*\")))\\s*))*)?)\\)\\s*)?)(?:]]|}})","g");function Y(e){let t="";for(let r=0;r<e.length;r++){t+=e[r].literal||""}return t}function V(e){let t=e.match(/([^\s]+?)\(([\s\S]*)\)/);if(t){let e={methodName:t[1],static:!0,args:J};if(t[2].trim()){return function(e,t){return t.args=e.map((function(e){let r=W(e);return r.literal||(t.static=!1),r}),this),t}(t[2].replace(/\\,/g,"&comma;").split(","),e)}return e}return null}function W(e){let t=e.trim().replace(/&comma;/g,",").replace(/\\(.)/g,"$1"),r={name:t,value:"",literal:!1},n=t[0];switch("-"===n&&(n=t[1]),n>="0"&&n<="9"&&(n="#"),n){case"'":case'"':r.value=t.slice(1,-1),r.literal=!0;break;case"#":r.value=Number(t),r.literal=!0}return r.literal||(r.rootProperty=(0,i.Jz)(t),r.structured=(0,i.AZ)(t),r.structured&&(r.wildcard=".*"==t.slice(-2),r.wildcard&&(r.name=t.slice(0,-2)))),r}function G(e,t,r){let n=(0,i.U2)(e,r);return void 0===n&&(n=t[r]),n}function Z(e,t,r,n){const s={indexSplices:n};g.HY&&!e._overrideLegacyUndefined&&(t.splices=s),e.notifyPath(r+".splices",s),e.notifyPath(r+".length",t.length),g.HY&&!e._overrideLegacyUndefined&&(s.indexSplices=[])}function X(e,t,r,n,s,i){Z(e,t,r,[{index:n,addedCount:s,removed:i,object:t,type:"splice"}])}const K=(0,s.o)((e=>{const t=y((0,o.Q)(e));return class extends t{constructor(){super(),this.__isPropertyEffectsClient=!0,this.__dataClientsReady,this.__dataPendingClients,this.__dataToNotify,this.__dataLinkedPaths,this.__dataHasPaths,this.__dataCompoundStorage,this.__dataHost,this.__dataTemp,this.__dataClientsInitialized,this.__data,this.__dataPending,this.__dataOld,this.__computeEffects,this.__computeInfo,this.__reflectEffects,this.__notifyEffects,this.__propagateEffects,this.__observeEffects,this.__readOnly,this.__templateInfo,this._overrideLegacyUndefined}get PROPERTY_EFFECT_TYPES(){return w}_initializeProperties(){super._initializeProperties(),this._registerHost(),this.__dataClientsReady=!1,this.__dataPendingClients=null,this.__dataToNotify=null,this.__dataLinkedPaths=null,this.__dataHasPaths=!1,this.__dataCompoundStorage=this.__dataCompoundStorage||null,this.__dataHost=this.__dataHost||null,this.__dataTemp={},this.__dataClientsInitialized=!1}_registerHost(){if(Q.length){let e=Q[Q.length-1];e._enqueueClient(this),this.__dataHost=e}}_initializeProtoProperties(e){this.__data=Object.create(e),this.__dataPending=Object.create(e),this.__dataOld={}}_initializeInstanceProperties(e){let t=this[w.READ_ONLY];for(let r in e)t&&t[r]||(this.__dataPending=this.__dataPending||{},this.__dataOld=this.__dataOld||{},this.__data[r]=this.__dataPending[r]=e[r])}_addPropertyEffect(e,t,r){this._createPropertyAccessor(e,t==w.READ_ONLY);let n=S(this,t,!0)[e];n||(n=this[t][e]=[]),n.push(r)}_removePropertyEffect(e,t,r){let n=S(this,t,!0)[e],s=n.indexOf(r);s>=0&&n.splice(s,1)}_hasPropertyEffect(e,t){let r=this[t];return Boolean(r&&r[e])}_hasReadOnlyEffect(e){return this._hasPropertyEffect(e,w.READ_ONLY)}_hasNotifyEffect(e){return this._hasPropertyEffect(e,w.NOTIFY)}_hasReflectEffect(e){return this._hasPropertyEffect(e,w.REFLECT)}_hasComputedEffect(e){return this._hasPropertyEffect(e,w.COMPUTE)}_setPendingPropertyOrPath(e,t,r,n){if(n||(0,i.Jz)(Array.isArray(e)?e[0]:e)!==e){if(!n){let r=(0,i.U2)(this,e);if(!(e=(0,i.t8)(this,e,t))||!super._shouldPropertyChange(e,t,r))return!1}if(this.__dataHasPaths=!0,this._setPendingProperty(e,t,r))return function(e,t,r){let n=e.__dataLinkedPaths;if(n){let s;for(let a in n){let o=n[a];(0,i.SG)(a,t)?(s=(0,i.Iu)(a,o,t),e._setPendingPropertyOrPath(s,r,!0,!0)):(0,i.SG)(o,t)&&(s=(0,i.Iu)(o,a,t),e._setPendingPropertyOrPath(s,r,!0,!0))}}}(this,e,t),!0}else{if(this.__dataHasAccessor&&this.__dataHasAccessor[e])return this._setPendingProperty(e,t,r);this[e]=t}return!1}_setUnmanagedPropertyToNode(e,t,r){r===e[t]&&"object"!=typeof r||("className"===t&&(e=(0,n.r)(e)),e[t]=r)}_setPendingProperty(e,t,r){let n=this.__dataHasPaths&&(0,i.AZ)(e),s=n?this.__dataTemp:this.__data;return!!this._shouldPropertyChange(e,t,s[e])&&(this.__dataPending||(this.__dataPending={},this.__dataOld={}),e in this.__dataOld||(this.__dataOld[e]=this.__data[e]),n?this.__dataTemp[e]=t:this.__data[e]=t,this.__dataPending[e]=t,(n||this[w.NOTIFY]&&this[w.NOTIFY][e])&&(this.__dataToNotify=this.__dataToNotify||{},this.__dataToNotify[e]=r),!0)}_setProperty(e,t){this._setPendingProperty(e,t,!0)&&this._invalidateProperties()}_invalidateProperties(){this.__dataReady&&this._flushProperties()}_enqueueClient(e){this.__dataPendingClients=this.__dataPendingClients||[],e!==this&&this.__dataPendingClients.push(e)}_flushClients(){this.__dataClientsReady?this.__enableOrFlushClients():(this.__dataClientsReady=!0,this._readyClients(),this.__dataReady=!0)}__enableOrFlushClients(){let e=this.__dataPendingClients;if(e){this.__dataPendingClients=null;for(let t=0;t<e.length;t++){let r=e[t];r.__dataEnabled?r.__dataPending&&r._flushProperties():r._enableProperties()}}}_readyClients(){this.__enableOrFlushClients()}setProperties(e,t){for(let r in e)!t&&this[w.READ_ONLY]&&this[w.READ_ONLY][r]||this._setPendingPropertyOrPath(r,e[r],!0);this._invalidateProperties()}ready(){this._flushProperties(),this.__dataClientsReady||this._flushClients(),this.__dataPending&&this._flushProperties()}_propertiesChanged(e,t,r){let n,s=this.__dataHasPaths;this.__dataHasPaths=!1,R(this,t,r,s),n=this.__dataToNotify,this.__dataToNotify=null,this._propagatePropertyChanges(t,r,s),this._flushClients(),v(this,this[w.REFLECT],t,r,s),v(this,this[w.OBSERVE],t,r,s),n&&function(e,t,r,n,s){let i,a,o=e[w.NOTIFY],l=b++;for(let a in t)t[a]&&(o&&E(e,o,l,a,r,n,s)||s&&T(e,a,r))&&(i=!0);i&&(a=e.__dataHost)&&a._invalidateProperties&&a._invalidateProperties()}(this,n,t,r,s),1==this.__dataCounter&&(this.__dataTemp={})}_propagatePropertyChanges(e,t,r){this[w.PROPAGATE]&&v(this,this[w.PROPAGATE],e,t,r),this.__templateInfo&&this._runEffectsForTemplate(this.__templateInfo,e,t,r)}_runEffectsForTemplate(e,t,r,n){const s=(t,n)=>{v(this,e.propertyEffects,t,r,n,e.nodeList);for(let s=e.firstChild;s;s=s.nextSibling)this._runEffectsForTemplate(s,t,r,n)};e.runEffects?e.runEffects(s,t,n):s(t,n)}linkPaths(e,t){e=(0,i.Fv)(e),t=(0,i.Fv)(t),this.__dataLinkedPaths=this.__dataLinkedPaths||{},this.__dataLinkedPaths[e]=t}unlinkPaths(e){e=(0,i.Fv)(e),this.__dataLinkedPaths&&delete this.__dataLinkedPaths[e]}notifySplices(e,t){let r={path:""};Z(this,(0,i.U2)(this,e,r),r.path,t)}get(e,t){return(0,i.U2)(t||this,e)}set(e,t,r){r?(0,i.t8)(r,e,t):this[w.READ_ONLY]&&this[w.READ_ONLY][e]||this._setPendingPropertyOrPath(e,t,!0)&&this._invalidateProperties()}push(e,...t){let r={path:""},n=(0,i.U2)(this,e,r),s=n.length,a=n.push(...t);return t.length&&X(this,n,r.path,s,t.length,[]),a}pop(e){let t={path:""},r=(0,i.U2)(this,e,t),n=Boolean(r.length),s=r.pop();return n&&X(this,r,t.path,r.length,0,[s]),s}splice(e,t,r,...n){let s,a={path:""},o=(0,i.U2)(this,e,a);return t<0?t=o.length-Math.floor(-t):t&&(t=Math.floor(t)),s=2===arguments.length?o.splice(t):o.splice(t,r,...n),(n.length||s.length)&&X(this,o,a.path,t,n.length,s),s}shift(e){let t={path:""},r=(0,i.U2)(this,e,t),n=Boolean(r.length),s=r.shift();return n&&X(this,r,t.path,0,0,[s]),s}unshift(e,...t){let r={path:""},n=(0,i.U2)(this,e,r),s=n.unshift(...t);return t.length&&X(this,n,r.path,0,t.length,[]),s}notifyPath(e,t){let r;if(1==arguments.length){let n={path:""};t=(0,i.U2)(this,e,n),r=n.path}else r=Array.isArray(e)?(0,i.Fv)(e):e;this._setPendingPropertyOrPath(r,t,!0,!0)&&this._invalidateProperties()}_createReadOnlyProperty(e,t){var r;this._addPropertyEffect(e,w.READ_ONLY),t&&(this["_set"+(r=e,r[0].toUpperCase()+r.substring(1))]=function(t){this._setProperty(e,t)})}_createPropertyObserver(e,t,r){let n={property:e,method:t,dynamicFn:Boolean(r)};this._addPropertyEffect(e,w.OBSERVE,{fn:O,info:n,trigger:{name:e}}),r&&this._addPropertyEffect(t,w.OBSERVE,{fn:O,info:n,trigger:{name:t}})}_createMethodObserver(e,t){let r=V(e);if(!r)throw new Error("Malformed observer expression '"+e+"'");$(this,r,w.OBSERVE,U,null,t)}_createNotifyingProperty(e){this._addPropertyEffect(e,w.NOTIFY,{fn:I,info:{eventName:(0,a.n)(e)+"-changed",property:e}})}_createReflectedProperty(e){let t=this.constructor.attributeNameForProperty(e);"-"===t[0]?console.warn("Property "+e+" cannot be reflected to attribute "+t+' because "-" is not a valid starting attribute name. Use a lowercase first letter for the property instead.'):this._addPropertyEffect(e,w.REFLECT,{fn:N,info:{attrName:t}})}_createComputedProperty(e,t,r){let n=V(t);if(!n)throw new Error("Malformed computed expression '"+t+"'");const s=$(this,n,w.COMPUTE,L,e,r);S(this,x)[e]=s}_marshalArgs(e,t,r){const n=this.__data,s=[];for(let a=0,o=e.length;a<o;a++){let{name:o,structured:l,wildcard:p,value:d,literal:c}=e[a];if(!c)if(p){const e=(0,i.SG)(o,t),s=G(n,r,e?t:o);d={path:e?t:o,value:s,base:e?(0,i.U2)(n,o):s}}else d=l?G(n,r,o):n[o];if(g.HY&&!this._overrideLegacyUndefined&&void 0===d&&e.length>1)return C;s[a]=d}return s}static addPropertyEffect(e,t,r){this.prototype._addPropertyEffect(e,t,r)}static createPropertyObserver(e,t,r){this.prototype._createPropertyObserver(e,t,r)}static createMethodObserver(e,t){this.prototype._createMethodObserver(e,t)}static createNotifyingProperty(e){this.prototype._createNotifyingProperty(e)}static createReadOnlyProperty(e,t){this.prototype._createReadOnlyProperty(e,t)}static createReflectedProperty(e){this.prototype._createReflectedProperty(e)}static createComputedProperty(e,t,r){this.prototype._createComputedProperty(e,t,r)}static bindTemplate(e){return this.prototype._bindTemplate(e)}_bindTemplate(e,t){let r=this.constructor._parseTemplate(e),n=this.__preBoundTemplateInfo==r;if(!n)for(let e in r.propertyEffects)this._createPropertyAccessor(e);if(t)if(r=Object.create(r),r.wasPreBound=n,this.__templateInfo){const t=e._parentTemplateInfo||this.__templateInfo,n=t.lastChild;r.parent=t,t.lastChild=r,r.previousSibling=n,n?n.nextSibling=r:t.firstChild=r}else this.__templateInfo=r;else this.__preBoundTemplateInfo=r;return r}static _addTemplatePropertyEffect(e,t,r){(e.hostProps=e.hostProps||{})[t]=!0;let n=e.propertyEffects=e.propertyEffects||{};(n[t]=n[t]||[]).push(r)}_stampTemplate(e,t){t=t||this._bindTemplate(e,!0),Q.push(this);let r=super._stampTemplate(e,t);if(Q.pop(),t.nodeList=r.nodeList,!t.wasPreBound){let e=t.childNodes=[];for(let t=r.firstChild;t;t=t.nextSibling)e.push(t)}return r.templateInfo=t,function(e,t){let{nodeList:r,nodeInfoList:n}=t;if(n.length)for(let t=0;t<n.length;t++){let s=n[t],i=r[t],a=s.bindings;if(a)for(let t=0;t<a.length;t++){let r=a[t];H(i,r),B(i,e,r)}i.__dataHost=e}}(this,t),this.__dataClientsReady&&(this._runEffectsForTemplate(t,this.__data,null,!1),this._flushClients()),r}_removeBoundDom(e){const t=e.templateInfo,{previousSibling:r,nextSibling:s,parent:i}=t;r?r.nextSibling=s:i&&(i.firstChild=s),s?s.previousSibling=r:i&&(i.lastChild=r),t.nextSibling=t.previousSibling=null;let a=t.childNodes;for(let e=0;e<a.length;e++){let t=a[e];(0,n.r)((0,n.r)(t).parentNode).removeChild(t)}}static _parseTemplateNode(e,r,n){let s=t._parseTemplateNode.call(this,e,r,n);if(e.nodeType===Node.TEXT_NODE){let t=this._parseBindings(e.textContent,r);t&&(e.textContent=Y(t)||" ",F(this,r,n,"text","textContent",t),s=!0)}return s}static _parseTemplateNodeAttribute(e,r,n,s,i){let o=this._parseBindings(i,r);if(o){let t=s,i="property";P.test(s)?i="attribute":"$"==s[s.length-1]&&(s=s.slice(0,-1),i="attribute");let l=Y(o);return l&&"attribute"==i&&("class"==s&&e.hasAttribute("class")&&(l+=" "+e.getAttribute(s)),e.setAttribute(s,l)),"attribute"==i&&"disable-upgrade$"==t&&e.setAttribute(s,""),"input"===e.localName&&"value"===t&&e.setAttribute(t,""),e.removeAttribute(t),"property"===i&&(s=(0,a.z)(s)),F(this,r,n,i,s,o,l),!0}return t._parseTemplateNodeAttribute.call(this,e,r,n,s,i)}static _parseTemplateNestedTemplate(e,r,n){let s=t._parseTemplateNestedTemplate.call(this,e,r,n);const i=e.parentNode,a=n.templateInfo,o="dom-if"===i.localName,l="dom-repeat"===i.localName;g.gx&&(o||l)&&(i.removeChild(e),(n=n.parentInfo).templateInfo=a,n.noted=!0,s=!1);let p=a.hostProps;if(g.ew&&o)p&&(r.hostProps=Object.assign(r.hostProps||{},p),g.gx||(n.parentInfo.noted=!0));else{let e="{";for(let t in p){F(this,r,n,"property","_host_"+t,[{mode:e,source:t,dependencies:[t],hostProp:!0}])}}return s}static _parseBindings(e,t){let r,n=[],s=0;for(;null!==(r=q.exec(e));){r.index>s&&n.push({literal:e.slice(s,r.index)});let i=r[1][0],a=Boolean(r[2]),o=r[3].trim(),l=!1,p="",d=-1;"{"==i&&(d=o.indexOf("::"))>0&&(p=o.substring(d+2),o=o.substring(0,d),l=!0);let c=V(o),h=[];if(c){let{args:e,methodName:r}=c;for(let t=0;t<e.length;t++){let r=e[t];r.literal||h.push(r)}let n=t.dynamicFns;(n&&n[r]||c.static)&&(h.push(r),c.dynamicFn=!0)}else h.push(o);n.push({source:o,mode:i,negate:a,customEvent:l,signature:c,dependencies:h,event:p}),s=q.lastIndex}if(s&&s<e.length){let t=e.substring(s);t&&n.push({literal:t})}return n.length?n:null}static _evaluateBinding(e,t,r,n,s,a){let o;return o=t.signature?U(e,r,n,0,t.signature):r!=t.source?(0,i.U2)(e,t.source):a&&(0,i.AZ)(r)?(0,i.U2)(e,r):e.__data[r],t.negate&&(o=!o),o}}})),Q=[]},4507:(e,t,r)=>{r.d(t,{c:()=>i});r(56646);function n(e,t,r){return{index:e,removed:t,addedCount:r}}function s(e,t,r,s,i,o){let l,p=0,d=0,c=Math.min(r-t,o-i);if(0==t&&0==i&&(p=function(e,t,r){for(let n=0;n<r;n++)if(!a(e[n],t[n]))return n;return r}(e,s,c)),r==e.length&&o==s.length&&(d=function(e,t,r){let n=e.length,s=t.length,i=0;for(;i<r&&a(e[--n],t[--s]);)i++;return i}(e,s,c-p)),i+=p,o-=d,(r-=d)-(t+=p)==0&&o-i==0)return[];if(t==r){for(l=n(t,[],0);i<o;)l.removed.push(s[i++]);return[l]}if(i==o)return[n(t,[],r-t)];let h=function(e){let t=e.length-1,r=e[0].length-1,n=e[t][r],s=[];for(;t>0||r>0;){if(0==t){s.push(2),r--;continue}if(0==r){s.push(3),t--;continue}let i,a=e[t-1][r-1],o=e[t-1][r],l=e[t][r-1];i=o<l?o<a?o:a:l<a?l:a,i==a?(a==n?s.push(0):(s.push(1),n=a),t--,r--):i==o?(s.push(3),t--,n=o):(s.push(2),r--,n=l)}return s.reverse(),s}(function(e,t,r,n,s,i){let o=i-s+1,l=r-t+1,p=new Array(o);for(let e=0;e<o;e++)p[e]=new Array(l),p[e][0]=e;for(let e=0;e<l;e++)p[0][e]=e;for(let r=1;r<o;r++)for(let i=1;i<l;i++)if(a(e[t+i-1],n[s+r-1]))p[r][i]=p[r-1][i-1];else{let e=p[r-1][i]+1,t=p[r][i-1]+1;p[r][i]=e<t?e:t}return p}(e,t,r,s,i,o));l=void 0;let u=[],_=t,f=i;for(let e=0;e<h.length;e++)switch(h[e]){case 0:l&&(u.push(l),l=void 0),_++,f++;break;case 1:l||(l=n(_,[],0)),l.addedCount++,_++,l.removed.push(s[f]),f++;break;case 2:l||(l=n(_,[],0)),l.addedCount++,_++;break;case 3:l||(l=n(_,[],0)),l.removed.push(s[f]),f++}return l&&u.push(l),u}function i(e,t){return s(e,0,e.length,t,0,t.length)}function a(e,t){return e===t}},56646:()=>{window.JSCompiler_renameProperty=function(e,t){return e}},67130:(e,t,r)=>{r.d(t,{z:()=>a,n:()=>o});r(56646);const n={},s=/-[a-z]/g,i=/([A-Z])/g;function a(e){return n[e]||(n[e]=e.indexOf("-")<0?e:e.replace(s,(e=>e[1].toUpperCase())))}function o(e){return n[e]||(n[e]=e.replace(i,"-$1").toLowerCase())}},78956:(e,t,r)=>{r.d(t,{dx:()=>n,Ex:()=>i,Jk:()=>a});r(56646),r(76389),r(21683);class n{constructor(){this._asyncModule=null,this._callback=null,this._timer=null}setConfig(e,t){this._asyncModule=e,this._callback=t,this._timer=this._asyncModule.run((()=>{this._timer=null,s.delete(this),this._callback()}))}cancel(){this.isActive()&&(this._cancelAsync(),s.delete(this))}_cancelAsync(){this.isActive()&&(this._asyncModule.cancel(this._timer),this._timer=null)}flush(){this.isActive()&&(this.cancel(),this._callback())}isActive(){return null!=this._timer}static debounce(e,t,r){return e instanceof n?e._cancelAsync():e=new n,e.setConfig(t,r),e}}let s=new Set;const i=function(e){s.add(e)},a=function(){const e=Boolean(s.size);return s.forEach((e=>{try{e.flush()}catch(e){setTimeout((()=>{throw e}))}})),e}},20723:(e,t,r)=>{r.d(t,{o:()=>o});r(56646);var n=r(4507),s=r(21683),i=r(62276);function a(e){return"slot"===e.localName}let o=class{static getFlattenedNodes(e){const t=(0,i.r)(e);return a(e)?(e=e,t.assignedNodes({flatten:!0})):Array.from(t.childNodes).map((e=>a(e)?(e=e,(0,i.r)(e).assignedNodes({flatten:!0})):[e])).reduce(((e,t)=>e.concat(t)),[])}constructor(e,t){this._shadyChildrenObserver=null,this._nativeChildrenObserver=null,this._connected=!1,this._target=e,this.callback=t,this._effectiveNodes=[],this._observer=null,this._scheduled=!1,this._boundSchedule=()=>{this._schedule()},this.connect(),this._schedule()}connect(){a(this._target)?this._listenSlots([this._target]):(0,i.r)(this._target).children&&(this._listenSlots((0,i.r)(this._target).children),window.ShadyDOM?this._shadyChildrenObserver=window.ShadyDOM.observeChildren(this._target,(e=>{this._processMutations(e)})):(this._nativeChildrenObserver=new MutationObserver((e=>{this._processMutations(e)})),this._nativeChildrenObserver.observe(this._target,{childList:!0}))),this._connected=!0}disconnect(){a(this._target)?this._unlistenSlots([this._target]):(0,i.r)(this._target).children&&(this._unlistenSlots((0,i.r)(this._target).children),window.ShadyDOM&&this._shadyChildrenObserver?(window.ShadyDOM.unobserveChildren(this._shadyChildrenObserver),this._shadyChildrenObserver=null):this._nativeChildrenObserver&&(this._nativeChildrenObserver.disconnect(),this._nativeChildrenObserver=null)),this._connected=!1}_schedule(){this._scheduled||(this._scheduled=!0,s.YA.run((()=>this.flush())))}_processMutations(e){this._processSlotMutations(e),this.flush()}_processSlotMutations(e){if(e)for(let t=0;t<e.length;t++){let r=e[t];r.addedNodes&&this._listenSlots(r.addedNodes),r.removedNodes&&this._unlistenSlots(r.removedNodes)}}flush(){if(!this._connected)return!1;window.ShadyDOM&&ShadyDOM.flush(),this._nativeChildrenObserver?this._processSlotMutations(this._nativeChildrenObserver.takeRecords()):this._shadyChildrenObserver&&this._processSlotMutations(this._shadyChildrenObserver.takeRecords()),this._scheduled=!1;let e={target:this._target,addedNodes:[],removedNodes:[]},t=this.constructor.getFlattenedNodes(this._target),r=(0,n.c)(t,this._effectiveNodes);for(let t,n=0;n<r.length&&(t=r[n]);n++)for(let r,n=0;n<t.removed.length&&(r=t.removed[n]);n++)e.removedNodes.push(r);for(let n,s=0;s<r.length&&(n=r[s]);s++)for(let r=n.index;r<n.index+n.addedCount;r++)e.addedNodes.push(t[r]);this._effectiveNodes=t;let s=!1;return(e.addedNodes.length||e.removedNodes.length)&&(s=!0,this.callback.call(this._target,e)),s}_listenSlots(e){for(let t=0;t<e.length;t++){let r=e[t];a(r)&&r.addEventListener("slotchange",this._boundSchedule)}}_unlistenSlots(e){for(let t=0;t<e.length;t++){let r=e[t];a(r)&&r.removeEventListener("slotchange",this._boundSchedule)}}}},93252:(e,t,r)=>{r.d(t,{E:()=>n.Ex,y:()=>s});r(56646);var n=r(78956);const s=function(){let e,t;do{e=window.ShadyDOM&&ShadyDOM.flush(),window.ShadyCSS&&window.ShadyCSS.ScopingShim&&window.ShadyCSS.ScopingShim.flush(),t=(0,n.Jk)()}while(e||t)}},6226:(e,t,r)=>{r.d(t,{N:()=>i});var n=r(74460);let s=!1;function i(){if(n.nL&&!n.my){if(!s){s=!0;const e=document.createElement("style");e.textContent="dom-bind,dom-if,dom-repeat{display:none;}",document.head.appendChild(e)}return!0}return!1}},50856:(e,t,r)=>{r.d(t,{d:()=>i});r(56646);class n{constructor(e){this.value=e.toString()}toString(){return this.value}}function s(e){if(e instanceof n)return e.value;throw new Error(`non-literal value passed to Polymer's htmlLiteral function: ${e}`)}const i=function(e,...t){const r=document.createElement("template");return r.innerHTML=t.reduce(((t,r,i)=>t+function(e){if(e instanceof HTMLTemplateElement)return e.innerHTML;if(e instanceof n)return s(e);throw new Error(`non-template value passed to Polymer's html function: ${e}`)}(r)+e[i+1]),e[0]),r}},76389:(e,t,r)=>{r.d(t,{o:()=>i});r(56646);let n=0;function s(){}s.prototype.__mixinApplications,s.prototype.__mixinSet;const i=function(e){let t=e.__mixinApplications;t||(t=new WeakMap,e.__mixinApplications=t);let r=n++;return function(n){let s=n.__mixinSet;if(s&&s[r])return n;let i=t,a=i.get(n);if(!a){a=e(n),i.set(n,a);let t=Object.create(a.__mixinSet||s||null);t[r]=!0,a.__mixinSet=t}return a}}},4059:(e,t,r)=>{r.d(t,{AZ:()=>n,Jz:()=>s,jg:()=>i,SG:()=>a,Iu:()=>o,wB:()=>l,Fv:()=>p,U2:()=>c,t8:()=>h});r(56646);function n(e){return e.indexOf(".")>=0}function s(e){let t=e.indexOf(".");return-1===t?e:e.slice(0,t)}function i(e,t){return 0===e.indexOf(t+".")}function a(e,t){return 0===t.indexOf(e+".")}function o(e,t,r){return t+r.slice(e.length)}function l(e,t){return e===t||i(e,t)||a(e,t)}function p(e){if(Array.isArray(e)){let t=[];for(let r=0;r<e.length;r++){let n=e[r].toString().split(".");for(let e=0;e<n.length;e++)t.push(n[e])}return t.join(".")}return e}function d(e){return Array.isArray(e)?p(e).split("."):e.toString().split(".")}function c(e,t,r){let n=e,s=d(t);for(let e=0;e<s.length;e++){if(!n)return;n=n[s[e]]}return r&&(r.path=s.join(".")),n}function h(e,t,r){let n=e,s=d(t),i=s[s.length-1];if(s.length>1){for(let e=0;e<s.length-1;e++){if(n=n[s[e]],!n)return}n[i]=r}else n[t]=r;return s.join(".")}},42687:(e,t,r)=>{r.d(t,{Kk:()=>o,Rq:()=>l,iY:()=>p});r(56646);let n,s,i=/(url\()([^)]*)(\))/g,a=/(^\/[^\/])|(^#)|(^[\w-\d]*:)/;function o(e,t){if(e&&a.test(e))return e;if("//"===e)return e;if(void 0===n){n=!1;try{const e=new URL("b","http://a");e.pathname="c%20d",n="http://a/c%20d"===e.href}catch(e){}}if(t||(t=document.baseURI||window.location.href),n)try{return new URL(e,t).href}catch(t){return e}return s||(s=document.implementation.createHTMLDocument("temp"),s.base=s.createElement("base"),s.head.appendChild(s.base),s.anchor=s.createElement("a"),s.body.appendChild(s.anchor)),s.base.href=t,s.anchor.href=e,s.anchor.href||e}function l(e,t){return e.replace(i,(function(e,r,n,s){return r+"'"+o(n.replace(/["']/g,""),t)+"'"+s}))}function p(e){return e.substring(0,e.lastIndexOf("/")+1)}},15392:(e,t,r)=>{r.d(t,{uT:()=>d,lx:()=>c,jv:()=>u});var n=r(21384),s=r(42687);const i="shady-unscoped";function a(e){return n.t.import(e)}function o(e){let t=e.body?e.body:e;const r=(0,s.Rq)(t.textContent,e.baseURI),n=document.createElement("style");return n.textContent=r,n}function l(e){const t=e.trim().split(/\s+/),r=[];for(let e=0;e<t.length;e++)r.push(...p(t[e]));return r}function p(e){const t=a(e);if(!t)return console.warn("Could not find style data in module named",e),[];if(void 0===t._styles){const e=[];e.push(...h(t));const r=t.querySelector("template");r&&e.push(...d(r,t.assetpath)),t._styles=e}return t._styles}function d(e,t){if(!e._styles){const r=[],n=e.content.querySelectorAll("style");for(let e=0;e<n.length;e++){let i=n[e],a=i.getAttribute("include");a&&r.push(...l(a).filter((function(e,t,r){return r.indexOf(e)===t}))),t&&(i.textContent=(0,s.Rq)(i.textContent,t)),r.push(i)}e._styles=r}return e._styles}function c(e){let t=a(e);return t?h(t):[]}function h(e){const t=[],r=e.querySelectorAll("link[rel=import][type~=css]");for(let e=0;e<r.length;e++){let n=r[e];if(n.import){const e=n.import,r=n.hasAttribute(i);if(r&&!e._unscopedStyle){const t=o(e);t.setAttribute(i,""),e._unscopedStyle=t}else e._style||(e._style=o(e));t.push(r?e._unscopedStyle:e._style)}}return t}function u(e){let t=e.trim().split(/\s+/),r="";for(let e=0;e<t.length;e++)r+=_(t[e]);return r}function _(e){let t=a(e);if(t&&void 0===t._cssText){let e=f(t),r=t.querySelector("template");r&&(e+=function(e,t){let r="";const n=d(e,t);for(let e=0;e<n.length;e++){let t=n[e];t.parentNode&&t.parentNode.removeChild(t),r+=t.textContent}return r}(r,t.assetpath)),t._cssText=e||null}return t||console.warn("Could not find style data in module named",e),t&&t._cssText||""}function f(e){let t="",r=h(e);for(let e=0;e<r.length;e++)t+=r[e].textContent;return t}},65412:(e,t,r)=>{r.d(t,{Gd:()=>n,z2:()=>i});function n(){0}const s=[];function i(e){s.push(e)}},62276:(e,t,r)=>{r.d(t,{r:()=>n});const n=window.ShadyDOM&&window.ShadyDOM.noPatch&&window.ShadyDOM.wrap?window.ShadyDOM.wrap:window.ShadyDOM?e=>ShadyDOM.patch(e):e=>e},60309:(e,t,r)=>{r.d(t,{CN:()=>n,$T:()=>s,mA:()=>i});const n=/(?:^|[;\s{]\s*)(--[\w-]*?)\s*:\s*(?:((?:'(?:\\'|.)*?'|"(?:\\"|.)*?"|\([^)]*?\)|[^};{])+)|\{([^}]*)\}(?:(?=[;\s}])|$))/gi,s=/(?:^|\W+)@apply\s*\(?([^);\n]*)\)?/gi,i=/@media\s(.*)/},10868:(e,t,r)=>{r.d(t,{wW:()=>s,B7:()=>i,OH:()=>a});var n=r(60309);function s(e,t){for(let r in t)null===r?e.style.removeProperty(r):e.style.setProperty(r,t[r])}function i(e,t){const r=window.getComputedStyle(e).getPropertyValue(t);return r?r.trim():""}function a(e){const t=n.$T.test(e)||n.CN.test(e);return n.$T.lastIndex=0,n.CN.lastIndex=0,t}},34816:(e,t,r)=>{r.d(t,{ZP:()=>c});let n,s=null,i=window.HTMLImports&&window.HTMLImports.whenReady||null;function a(e){requestAnimationFrame((function(){i?i(e):(s||(s=new Promise((e=>{n=e})),"complete"===document.readyState?n():document.addEventListener("readystatechange",(()=>{"complete"===document.readyState&&n()}))),s.then((function(){e&&e()})))}))}const o="__seenByShadyCSS",l="__shadyCSSCachedStyle";let p=null,d=null;class c{constructor(){this.customStyles=[],this.enqueued=!1,a((()=>{window.ShadyCSS.flushCustomStyles&&window.ShadyCSS.flushCustomStyles()}))}enqueueDocumentValidation(){!this.enqueued&&d&&(this.enqueued=!0,a(d))}addCustomStyle(e){e[o]||(e[o]=!0,this.customStyles.push(e),this.enqueueDocumentValidation())}getStyleForCustomStyle(e){if(e[l])return e[l];let t;return t=e.getStyle?e.getStyle():e,t}processStyles(){const e=this.customStyles;for(let t=0;t<e.length;t++){const r=e[t];if(r[l])continue;const n=this.getStyleForCustomStyle(r);if(n){const e=n.__appliedElement||n;p&&p(e),r[l]=e}}return e}}c.prototype.addCustomStyle=c.prototype.addCustomStyle,c.prototype.getStyleForCustomStyle=c.prototype.getStyleForCustomStyle,c.prototype.processStyles=c.prototype.processStyles,Object.defineProperties(c.prototype,{transformCallback:{get:()=>p,set(e){p=e}},validateCallback:{get:()=>d,set(e){let t=!1;d||(t=!0),d=e,t&&this.enqueueDocumentValidation()}}})},26539:(e,t,r)=>{r.d(t,{WA:()=>n,Cp:()=>i,jF:()=>o,rd:()=>l});const n=!(window.ShadyDOM&&window.ShadyDOM.inUse);let s,i;function a(e){s=(!e||!e.shimcssproperties)&&(n||Boolean(!navigator.userAgent.match(/AppleWebKit\/601|Edge\/15/)&&window.CSS&&CSS.supports&&CSS.supports("box-shadow","0 0 0 var(--foo)")))}window.ShadyCSS&&void 0!==window.ShadyCSS.cssBuild&&(i=window.ShadyCSS.cssBuild);const o=Boolean(window.ShadyCSS&&window.ShadyCSS.disableRuntime);window.ShadyCSS&&void 0!==window.ShadyCSS.nativeCss?s=window.ShadyCSS.nativeCss:window.ShadyCSS?(a(window.ShadyCSS),window.ShadyCSS=void 0):a(window.WebComponents&&window.WebComponents.flags);const l=s}}]);
//# sourceMappingURL=f4f19070.js.map