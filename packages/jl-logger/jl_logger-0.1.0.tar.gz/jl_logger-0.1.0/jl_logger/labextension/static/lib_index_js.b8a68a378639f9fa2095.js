"use strict";
(self["webpackChunkjl_logger"] = self["webpackChunkjl_logger"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jl-logger', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ButtonExtension": () => (/* binding */ ButtonExtension),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");




const jlLoggerToolbarItemClassName = 'jl-logger-tools';
const activeJlLoggerBtnClassName = 'activated-jl-logger-btn';
/**
 * The plugin registration information.
 */
const jlLogger = {
    id: 'jl-logger',
    autoStart: true,
    activate: (app) => {
        app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension);
    }
};
class ButtonExtension {
    /**
     * Create a new extension for the notebook panel widget.
     *
     * @param panel Notebook panel
     * @param context Notebook context
     * @returns Disposable on the added button
     */
    createNew(panel, context) {
        /**
         * Append hidden element for determining activity of jl-logger.
         * @param notebookId
         */
        const appendJlLoggerHiddenElem = (notebookId) => {
            const e = document.createElement('input');
            e.setAttribute('type', 'hidden');
            e.id = 'jl-logger-' + notebookId;
            e.value = '0';
            document.body.appendChild(e);
        };
        /**
         * Append text input and checkbox next to the jl-logger button
         * @param elem
         * @param targetNotebookId
         */
        const appendToolbarItems = (elem, targetNotebookId) => {
            var _a;
            const parentSpanElem = document.createElement('span');
            parentSpanElem.className = jlLoggerToolbarItemClassName;
            const textInputElem = document.createElement('input');
            textInputElem.setAttribute('type', 'text');
            parentSpanElem.appendChild(textInputElem);
            const extSpanElem = document.createElement('span');
            extSpanElem.textContent = '.log';
            extSpanElem.className = 'ext-txt';
            parentSpanElem.append(extSpanElem);
            const wandbLabelElem = document.createElement('label');
            wandbLabelElem.textContent = 'W&B';
            wandbLabelElem.setAttribute('for', 'use-wandb-' + targetNotebookId);
            parentSpanElem.append(wandbLabelElem);
            const checkBoxElem = document.createElement('input');
            checkBoxElem.setAttribute('type', 'checkbox');
            checkBoxElem.id = 'use-wandb-' + targetNotebookId;
            parentSpanElem.appendChild(checkBoxElem);
            (_a = elem.parentElement) === null || _a === void 0 ? void 0 : _a.insertBefore(parentSpanElem, elem.nextSibling);
        };
        /**
         * switch activation of logger
         */
        const toggleActivation = () => {
            var _a, _b, _c, _d;
            const e = window.event;
            const targetNotebookId = document.getElementsByClassName('jp-mod-current')[0].getAttribute('data-id');
            let jlLoggerActivationElem = document.getElementById('jl-logger-' + targetNotebookId);
            if (jlLoggerActivationElem === null) {
                appendJlLoggerHiddenElem(targetNotebookId);
            }
            if (e !== undefined) {
                let elem = e.target;
                elem = (_c = (_b = (_a = elem.parentElement) === null || _a === void 0 ? void 0 : _a.parentElement) === null || _b === void 0 ? void 0 : _b.parentElement) === null || _c === void 0 ? void 0 : _c.getElementsByClassName('jl-logger-btn')[0].parentElement;
                elem.classList.toggle(activeJlLoggerBtnClassName);
                if (elem.classList.contains(activeJlLoggerBtnClassName)) {
                    appendToolbarItems(elem, targetNotebookId);
                    document.getElementById('jl-logger-' + targetNotebookId).value = '1';
                }
                else {
                    (_d = elem.parentElement) === null || _d === void 0 ? void 0 : _d.getElementsByClassName(jlLoggerToolbarItemClassName)[0].remove();
                    document.getElementById('jl-logger-' + targetNotebookId).value = '0';
                }
            }
        };
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            className: 'jl-logger-btn',
            label: 'Logger',
            onClick: toggleActivation,
            tooltip: 'Activate jl-logger',
        });
        panel.toolbar.insertItem(10, 'jl-logger', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
/**
 * Post request for logging.
 * @param logContents
 * @param filename
 */
const postLog = async (logContents, filename) => {
    const dataToSend = {
        logContent: logContents,
        filename: filename
    };
    try {
        const reply = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('LogOutputContent', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
        console.info(reply);
    }
    catch (reason) {
        console.error(`Error on POST /jl-logger/LogOutputContent ${dataToSend}.\n${reason}`);
    }
};
/**
 * Get string of current time.
 */
const getNowYMDhmsStr = () => {
    const date = new Date();
    const Y = date.getFullYear();
    const M = ("00" + (date.getMonth() + 1)).slice(-2);
    const D = ("00" + date.getDate()).slice(-2);
    const h = ("00" + date.getHours()).slice(-2);
    const m = ("00" + date.getMinutes()).slice(-2);
    return Y + M + D + h + m;
};
/**
 * Get content in output cells from OutputArea
 * @param outputArea
 * @returns
 */
const getOutputContents = (outputArea) => {
    const outputJSONArray = outputArea.model.toJSON();
    return outputJSONArray.map((v) => {
        let outputType = v.output_type;
        let logContent = '';
        switch (outputType) {
            case 'stream':
                logContent = '[' + outputType + ']' + '\n' + v.text;
                break;
            case 'execute_result':
                let data = v.data;
                let key = 'text/plain';
                if (Object.keys(data).includes(key)) {
                    logContent = '[' + outputType + ']' + '\n' + data[key] + '\n';
                }
                break;
            case 'error':
                logContent = '[' + outputType + ']' + '\n' + v.evalue + '\n';
                break;
        }
        return logContent;
    });
};
/**
 * Extract wandb run name from OutputArea
 * @param outputArea
 * @returns
 */
const extractWandbRunName = (outputArea) => {
    const outputJSONArray = outputArea.model.toJSON();
    let runName = '';
    let re = /(?<=<strong><a href="https:\/\/wandb\.ai\/.*>).*(?=.*<\/a><\/strong>)/;
    for (let v of outputJSONArray) {
        if (v.output_type === 'display_data') {
            let data = v.data;
            let key = 'text/html';
            if (Object.keys(data).includes(key)) {
                let res = re.exec(data[key]);
                if (res !== null) {
                    for (let s of res) {
                        runName = s;
                    }
                }
            }
        }
    }
    return runName;
};
_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookActions.executed.connect((_, action) => {
    const targetOutputArea = action.cell.outputArea;
    const outputContents = getOutputContents(targetOutputArea);
    const targetNotebookId = document.getElementsByClassName('jp-mod-current')[0].getAttribute('data-id');
    const targetNotbeoolElem = document.getElementById(targetNotebookId);
    const activeFlagElem = document.getElementById('jl-logger-' + targetNotebookId);
    if (activeFlagElem !== null && activeFlagElem.value === '1') {
        let specifiedFileName = targetNotbeoolElem.getElementsByClassName(jlLoggerToolbarItemClassName)[0].getElementsByTagName('input')[0].value;
        if (specifiedFileName === '' || specifiedFileName === null || specifiedFileName === undefined) {
            if (document.getElementById('use-wandb-' + targetNotebookId).checked) {
                const runName = extractWandbRunName(targetOutputArea);
                if (runName === null) {
                    specifiedFileName = getNowYMDhmsStr();
                }
                else {
                    targetNotbeoolElem.getElementsByClassName(jlLoggerToolbarItemClassName)[0].getElementsByTagName('input')[0].value = runName;
                    specifiedFileName = runName;
                }
            }
            else {
                specifiedFileName = getNowYMDhmsStr();
            }
        }
        postLog(outputContents, specifiedFileName);
    }
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (jlLogger);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b8a68a378639f9fa2095.js.map