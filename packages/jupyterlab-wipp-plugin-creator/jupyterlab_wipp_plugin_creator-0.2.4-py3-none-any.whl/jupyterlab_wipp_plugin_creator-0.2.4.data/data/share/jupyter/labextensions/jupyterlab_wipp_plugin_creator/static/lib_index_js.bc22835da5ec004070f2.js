"use strict";
(self["webpackChunkjupyterlab_wipp_plugin_creator"] = self["webpackChunkjupyterlab_wipp_plugin_creator"] || []).push([["lib_index_js"],{

/***/ "./lib/addedFilesWidget.js":
/*!*********************************!*\
  !*** ./lib/addedFilesWidget.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AddedFilesWidget": () => (/* binding */ AddedFilesWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _extensionConstants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./extensionConstants */ "./lib/extensionConstants.js");


class AddedFilesWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(state) {
        super();
        this._addedFileNames = [];
        this._state = state;
        this._addedFileDiv = document.createElement('p');
        this.node.appendChild(this._addedFileDiv);
        const button = document.createElement('button');
        button.innerHTML = 'Update list of files';
        button.onclick = () => this.update();
        this.node.appendChild(button);
        this.update();
    }
    onUpdateRequest(msg) {
        this._state.fetch(_extensionConstants__WEBPACK_IMPORTED_MODULE_1__.ExtensionConstants.dbkey).then(response => {
            this._addedFileNames = response;
            let text = 'Added Files: <br>';
            if (this._addedFileNames) {
                for (let i = 0; i < this._addedFileNames.length; i++) {
                    text += this._addedFileNames[i] + '<br>';
                }
            }
            this._addedFileDiv.innerHTML = text;
        });
    }
    getValue() {
        return this._addedFileNames;
    }
}


/***/ }),

/***/ "./lib/extensionConstants.js":
/*!***********************************!*\
  !*** ./lib/extensionConstants.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ExtensionConstants": () => (/* binding */ ExtensionConstants),
/* harmony export */   "addFilePathToDB": () => (/* binding */ addFilePathToDB)
/* harmony export */ });
class ExtensionConstants {
}
ExtensionConstants.dbkey = 'wipp-plugin-creator:data';
function addFilePathToDB(state, filepath) {
    state.fetch(ExtensionConstants.dbkey).then(response => {
        const filepaths = response;
        if (filepaths.indexOf(filepath) === -1) {
            filepaths.push(filepath);
        }
        else {
            console.log(`${filepath} was already added`);
        }
        state.save(ExtensionConstants.dbkey, filepaths);
    });
}


/***/ }),

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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab_wipp_plugin_creator', // API Namespace
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
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _extensionConstants__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./extensionConstants */ "./lib/extensionConstants.js");
/* harmony import */ var _sidebar__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./sidebar */ "./lib/sidebar.js");
/* harmony import */ var _style_logo_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/logo.svg */ "./style/logo.svg");








const logoIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.LabIcon({
    name: 'wipp-plugin-builder:logo',
    svgstr: _style_logo_svg__WEBPACK_IMPORTED_MODULE_5__["default"]
});
const filepaths = [];
const plugin = {
    id: 'jupyterlab_wipp_plugin_creator:plugin',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__.IStateDB, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager],
    activate: (app, factory, labShell, state, manager) => {
        // Initialzie dbkey if not in IStateDB
        state.list().then(response => {
            const keys = response.ids;
            if (keys.indexOf(_extensionConstants__WEBPACK_IMPORTED_MODULE_6__.ExtensionConstants.dbkey) === -1) {
                state.save(_extensionConstants__WEBPACK_IMPORTED_MODULE_6__.ExtensionConstants.dbkey, filepaths);
            }
        });
        // Create the WIPP sidebar panel
        const sidebar = new _sidebar__WEBPACK_IMPORTED_MODULE_7__.CreatorSidebar(state, manager);
        sidebar.id = 'wipp-labextension:plugin';
        sidebar.title.icon = logoIcon;
        sidebar.title.caption = 'WIPP Plugin Creator';
        labShell.add(sidebar, 'left', { rank: 200 });
        // Add context menu command, right click file browser to register marked files to be converted to plugin
        let filepath = '';
        const addFileToPluginContextMenuCommandID = 'wipp-plugin-creator-add-context-menu';
        app.commands.addCommand(addFileToPluginContextMenuCommandID, {
            label: 'Add to the new WIPP plugin',
            iconClass: 'jp-MaterialIcon jp-AddIcon',
            isVisible: () => ['notebook', 'file'].includes(factory.tracker.currentWidget.selectedItems().next().type),
            execute: () => {
                filepath = factory.tracker.currentWidget.selectedItems().next().path;
                (0,_extensionConstants__WEBPACK_IMPORTED_MODULE_6__.addFilePathToDB)(state, filepath);
            }
        });
        // Add command to context menu
        const selectorItem = '.jp-DirListing-item[data-isdir]';
        app.contextMenu.addItem({
            command: addFileToPluginContextMenuCommandID,
            selector: selectorItem
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/sidebar.js":
/*!************************!*\
  !*** ./lib/sidebar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CreatorSidebar": () => (/* binding */ CreatorSidebar)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @deathbeds/jupyterlab-rjsf */ "webpack/sharing/consume/default/@deathbeds/jupyterlab-rjsf/@deathbeds/jupyterlab-rjsf");
/* harmony import */ var _deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _addedFilesWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./addedFilesWidget */ "./lib/addedFilesWidget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _extensionConstants__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./extensionConstants */ "./lib/extensionConstants.js");
/* harmony import */ var _WippPluginSchema_json__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./WippPluginSchema.json */ "./lib/WippPluginSchema.json");








class CreatorSidebar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Create a new WIPP plugin creator sidebar.
     */
    constructor(state, manager) {
        super();
        this.addClass('wipp-pluginCreatorSidebar');
        // Define Widget layout
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout());
        const title = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        const h1 = document.createElement('h1');
        h1.innerText = 'Create New Plugin';
        title.node.appendChild(h1);
        layout.addWidget(title);
        // Necessary or plugin will not activate
        const schema = _WippPluginSchema_json__WEBPACK_IMPORTED_MODULE_4__;
        // Create file manager button
        const chooseFilesButtonWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        const chooseFilesButton = document.createElement('button');
        chooseFilesButton.className = 'run';
        chooseFilesButton.onclick = async () => {
            const dialog = _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.FileDialog.getOpenFiles({
                manager // IDocumentManager
            });
            const result = await dialog;
            if (result.button.accept) {
                const files = result.value;
                let filepath;
                if (files) {
                    for (let i = 0; i < files.length; i++) {
                        // files is a list of json,
                        // e.g. files[0]: Object { name: "pyproject.toml", path: "pyproject.toml" ..}
                        filepath = files[i]['path'];
                        (0,_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.addFilePathToDB)(state, filepath);
                    }
                }
                // log files object on 'Select' of the file manager
                console.log(files);
            }
        };
        chooseFilesButton.innerText = 'Choose Files';
        chooseFilesButtonWidget.node.appendChild(chooseFilesButton);
        layout.addWidget(chooseFilesButtonWidget);
        this._addFileWidget = new _addedFilesWidget__WEBPACK_IMPORTED_MODULE_6__.AddedFilesWidget(state);
        layout.addWidget(this._addFileWidget);
        const formData = {
            name: 'My Plugin',
            title: 'My Plugin',
            version: '0.1.0',
            description: '',
            author: '',
            institution: '',
            repository: '',
            website: '',
            citation: '',
            requirements: [''],
            inputs: [{}],
            outputs: [{}],
            baseImage: ''
        };
        const uiSchema = {
            name: {
                'ui:help': 'Hint: Enter human-readable name'
            },
            title: {
                'ui:help': 'Hint: Enter machine-readable name'
            },
            requirements: {
                'ui:help': `Hint: Enter 3rd party python packages that the plugin requires. Just the package name is fine for its latest version. To specify version: \r
          SomeProject == 1.3 \r
          SomeProject >=1.2,<2.0 \r
          SomeProject~=1.4.2 (~= means compatible, >=1.4.2, ==1.4.X)`
            },
            baseImage: {
                'ui:help': 'Hint: Choose the base image of the WIPP plugin to be created. Leave it as Python if unsure.'
            }
        };
        this._form = new _deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_3__.SchemaForm(schema, {
            formData: formData,
            uiSchema: uiSchema,
            liveValidate: true,
            noHtml5Validate: true
        }, { liveMarkdown: true });
        layout.addWidget(this._form);
        // Create submit plugin button
        const runButtonWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        const runButton = document.createElement('button');
        runButton.className = 'run';
        runButton.onclick = () => {
            this.submit();
        };
        runButton.innerText = 'Create Plugin';
        runButtonWidget.node.appendChild(runButton);
        layout.addWidget(runButtonWidget);
    }
    //Sidebar constructor ends
    submit() {
        //Create API request on submit
        const formValue = this._form.getValue();
        const request = {
            formdata: formValue.formData,
            addedfilepaths: this._addFileWidget.getValue()
        };
        if (formValue.errors !== null) {
            const fullRequest = {
                method: 'POST',
                body: JSON.stringify(request)
            };
            (0,_handler__WEBPACK_IMPORTED_MODULE_7__.requestAPI)('createplugin', fullRequest)
                .then(response => {
                console.log('POST request sent.');
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    body: 'Create Plugin request submitted. Building the plugin...',
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton()]
                });
            })
                .catch(() => {
                console.log('There is an error making POST CreatePlugin API request.');
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    body: 'There is an error making POST CreatePlugin API request.',
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton()]
                });
            });
        }
        else {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                body: 'There is an error with form value. Plugin build request failed.',
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton()]
            });
            console.log('Schema form data returns with an error');
            console.log(formValue.errors);
        }
    }
}


/***/ }),

/***/ "./style/logo.svg":
/*!************************!*\
  !*** ./style/logo.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"1792\" height=\"1792\" viewBox=\"0 0 1792 1792\" xmlns=\"http://www.w3.org/2000/svg\">\n    <path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M896 1629l640-349v-636l-640 233v752zm-64-865l698-254-698-254-698 254zm832-252v768q0 35-18 65t-49 47l-704 384q-28 16-61 16t-61-16l-704-384q-31-17-49-47t-18-65v-768q0-40 23-73t61-47l704-256q22-8 44-8t44 8l704 256q38 14 61 47t23 73z\"/>\n</svg> ");

/***/ }),

/***/ "./lib/WippPluginSchema.json":
/*!***********************************!*\
  !*** ./lib/WippPluginSchema.json ***!
  \***********************************/
/***/ ((module) => {

module.exports = JSON.parse('{"$schema":"http://json-schema.org/draft-07/schema#","$id":"https://raw.githubusercontent.com/usnistgov/WIPP-Plugins-base-templates/master/plugin-manifest/schema/wipp-plugin-manifest-schema.json","type":"object","title":"WIPP Plugin manifest","default":null,"required":["name","version","title","description","inputs","outputs"],"properties":{"name":{"$id":"#/properties/name","type":"string","title":"Name of the plugin","default":"","examples":["My Awesome Plugin"],"minLength":1,"pattern":"^(.*)$"},"requirements":{"type":"array","items":{"type":"string"},"title":"Requirements"},"version":{"$id":"#/properties/version","type":"string","title":"Plugin version","default":"","examples":["1.0.0"],"minLength":1,"pattern":"^(.*)$"},"title":{"$id":"#/properties/title","type":"string","title":"Plugin title","default":"","examples":["My really awesome plugin"],"minLength":1,"pattern":"^(.*)$"},"description":{"$id":"#/properties/description","type":"string","title":"Description","default":"","examples":["My awesome segmentation algorithm"],"minLength":1,"pattern":"^(.*)$"},"author":{"$id":"#/properties/author","type":["string","null"],"title":"Author(s)","default":"","examples":["FirstName LastName"],"pattern":"^(.*)$"},"institution":{"$id":"#/properties/institution","type":["string","null"],"title":"Institution","default":"","examples":["National Institute of Standards and Technology"],"pattern":"^(.*)$"},"repository":{"$id":"#/properties/repository","type":["string","null"],"title":"Source code repository","default":"","examples":["https://github.com/usnistgov/WIPP"],"format":"uri"},"website":{"$id":"#/properties/website","type":["string","null"],"title":"Website","default":"","examples":["http://usnistgov.github.io/WIPP"],"format":"uri"},"citation":{"$id":"#/properties/citation","type":["string","null"],"title":"Citation","default":"","examples":["Peter Bajcsy, Joe Chalfoun, and Mylene Simon (2018). Web Microanalysis of Big Image Data. Springer-Verlag International"],"pattern":"^(.*)$"},"inputs":{"$id":"#/properties/inputs","type":"array","title":"List of Inputs","description":"Defines inputs to the plugin","default":null,"uniqueItems":true,"items":{"$id":"#/properties/inputs/items","type":"object","title":"Input","description":"Plugin input","default":null,"required":["name","type","description"],"properties":{"name":{"$id":"#/properties/inputs/items/properties/name","type":"string","title":"Input name","description":"Input name as expected by the plugin CLI","default":"","examples":["inputImages","fileNamePattern","thresholdValue"],"pattern":"^[a-zA-Z0-9][-a-zA-Z0-9]*$"},"type":{"$id":"#/properties/inputs/items/properties/type","type":"string","enum":["collection","stitchingVector","tensorflowModel","csvCollection","pyramid","notebook","string","number","integer","enum","array","boolean"],"title":"Input Type","examples":["collection","string","number"]},"description":{"$id":"#/properties/inputs/items/properties/description","type":"string","title":"Input description","examples":["Input Images"],"pattern":"^(.*)$"},"required":{"$id":"#/properties/inputs/items/properties/required","type":"boolean","title":"Required input","description":"Whether an input is required or not","default":true,"examples":[true]}},"allOf":[{"if":{"properties":{"type":{"const":"enum"}}},"then":{"properties":{"options":{"$id":"#/properties/inputs/items/properties/options","type":"object","title":"Input options","properties":{"values":{"type":"array","description":"List of possible values","items":{"type":"string"},"uniqueItems":true}}}}}},{"if":{"properties":{"type":{"const":"array"}}},"then":{"properties":{"options":{"$id":"#/properties/inputs/items/properties/options","type":"object","title":"Input options","properties":{"items":{"$id":"#/properties/inputs/items/properties/options/properties/items","type":"object","title":"List of array items","description":"Possible values for the input array","default":{},"required":["type","title","oneOf","default","widget","minItems","uniqueItems"],"properties":{"type":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/type","type":"string","title":"Items type","description":"Type of the items to be selected","enum":["string"],"examples":["string"]},"title":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/title","type":"string","title":"Selection title","description":"Title of the item selection section in the form","default":"","examples":["Select feature"]},"oneOf":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf","type":"array","title":"Possible items","description":"List of possible items","default":[],"items":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items","type":"object","title":"Items definition","description":"Description of the possible items","default":{},"required":["description","enum"],"properties":{"description":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items/properties/description","type":"string","title":"Description","description":"Description of the value that will appear in the form","default":"","examples":["Area"]},"enum":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items/properties/enum","type":"array","title":"Value","description":"Values of the selected item","default":[],"items":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items/properties/enum/items","type":"string","title":"List of values","description":"List of values associated with the selected item (usually one value)","default":"","examples":["Feature2DJava_Area"]}}},"examples":[{"description":"Area","enum":["Feature2DJava_Area"]},{"enum":["Feature2DJava_Mean"],"description":"Mean"}]}},"default":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/default","type":"string","title":"Default value","description":"Value selected by default (must be one of the possible values)","default":"","examples":["Feature2DJava_Area"]},"widget":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/widget","type":"string","title":"Item selection widget","description":"How items can be selected (select -> dropdown list with add/remove buttons, checkbox -> multi-selection from list)","enum":["select","checkbox"],"examples":["select"]},"minItems":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/minItems","type":"integer","title":"Minumum number of items","description":"Minumum number of items","default":0,"examples":[1]},"uniqueItems":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/uniqueItems","type":["string","boolean"],"title":"Uniqueness of the items","description":"Whether items in the array have to be unique","examples":["true",true]}},"examples":[{"type":"string","widget":"select","uniqueItems":"true","default":"Feature2DJava_Area","minItems":1,"title":"Select feature","oneOf":[{"description":"Area","enum":["Feature2DJava_Area"]},{"description":"Mean","enum":["Feature2DJava_Mean"]}]}]}}}}}}]}},"outputs":{"$id":"#/properties/outputs","type":"array","title":"List of Outputs","description":"Defines the outputs of the plugin","default":null,"items":{"$id":"#/properties/outputs/items","type":"object","title":"Plugin output","default":null,"required":["name","type","description"],"properties":{"name":{"$id":"#/properties/outputs/items/properties/name","type":"string","title":"Output name","default":"","examples":["outputCollection"],"pattern":"^[a-zA-Z0-9][-a-zA-Z0-9]*$"},"type":{"$id":"#/properties/outputs/items/properties/type","type":"string","enum":["collection","stitchingVector","tensorflowModel","tensorboardLogs","csvCollection","pyramid"],"title":"Output type","examples":["stitchingVector","collection"]},"description":{"$id":"#/properties/outputs/items/properties/description","type":"string","title":"Output description","examples":["Output collection"],"pattern":"^(.*)$"}}}},"baseImage":{"$id":"#/properties/baseImage","type":"string","title":"Base Image of the plugin","default":"python","examples":["alpine:3.14"],"minLength":1,"pattern":"^(.*)$"}}}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.bc22835da5ec004070f2.js.map