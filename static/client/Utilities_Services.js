//js通用服务

//随机数
var randomIndex = Math.random();
var loadingStack = [];
angular.module('utilServices', []).factory('guid', function () {
    return {
        newGuid: function () {
            var guid = "";
            for (var i = 1; i <= 32; i++) {
                var n = Math.floor(Math.random() * 16.0).toString(16);
                guid += n;
                if ((i == 8) || (i == 12) || (i == 16) || (i == 20))
                    guid += "-";
            }
            return guid;
        },
        empty: function () {
            return "00000000-0000-0000-0000-000000000000";
        }
    };
})
.factory('confirmModal', ["$modal", function ($modal) {
    return {
        open: function (options) {
            var defaultOptions = {
               // confirmClick: function () { },
                text: '确认要执行此操作吗？'
            };

            extendOptions = angular.extend({}, defaultOptions, options);

            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/ConfirmModal.html?index=' + randomIndex,
                windowClass: 'dialogConfirm',
                controller: 'confirm',
                backdrop: 'static',
                resolve: {
                    options: function () {
                        return extendOptions;
                    }
                }
            });
            modalInstance.result.then(
               function () {
                   extendOptions.confirmClick();
               });
        }
    };
}])

.factory('errorModal', ["$modal", function ($modal) {
    return {
        open: function (errorList) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/ErrorModal.html' ,
                windowClass: 'dialogError',
                controller: 'error',
                backdrop: 'static',
                resolve: {
                    errorList: function () {
                        return errorList;
                    }
                }
            });
        }
    };
}])



.factory('alertModal', ["$modal", function ($modal) {
    return {
        open: function (message) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/AlertModal.html?index=' + randomIndex,
                windowClass: document.documentMode == 8 ? 'alertConfirmIE8' : 'alertConfirm',
                controller: 'alert',
                resolve: {
                    newMessage: function () {
                        return message;
                    }
                }
            });
            modalInstance.result.then(

               );
        }
    };
}])

.factory('loading', ["$rootScope", function ($rootScope) {
    return {
        open: function (text, scope) {
            var loadingText = "请稍候";
            var loadingScope = ".ui-content-main";
            var width = "";
            var height = "";
            if (arguments.length > 0 && text != null && text != '' && text != undefined) {
                loadingText = text;
            }
            if (arguments.length > 1) {
                loadingScope = scope;
            }
            if ($(loadingScope).children(".showFullLoading").length == 0) {
                width = $(loadingScope).width();
                height = $(loadingScope).height();

                $(loadingScope).prepend('<div class="showFullLoading" style="font-size: 22px;color:#444;height: ' + height + 'px; width: ' + width + 'px; position: absolute; z-index: 10000; background-color: transparent; text-align: center; padding-top: 100px;opacity:1;filter:alpha(opacity=100)"> \
                ' + loadingText + '...<i class="fa fa-2x fa-spinner fa-pulse"></i>\
               </div>');
            }
        },
        close: function (scope) {
            var loadingScope = ".ui-content-main";
            if (arguments.length > 0) {
                loadingScope = scope;
            }
            if ($(loadingScope).children(".showFullLoading").length > 0) {
                $(loadingScope).children(".showFullLoading").remove();
            }
        }
    };
}])


    ///options说明
    ///service:用于查询数据的服务，需要实现Query(queryString)方法
    ///title:弹出窗口的标题
    ///selectedItems:已经选择的项，数组类型，里面的项需要有id和name属性
    ///callBackFunc:弹出窗关闭时调用的方法，接收参数为所选择的项的数组
    ///multiSelect:是否允许多选
.factory('selectModal', ["$modal", function ($modal) {
    return {
        open: function (options) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/SelectModal.html?index=' + randomIndex,
                windowClass: 'AddOrgDialog',
                controller: 'select',
                backdrop: 'static',
                resolve: {
                    service: function () { return options.service },
                    title: function () { return options.title },
                    selectedItems: function () { return options.selectedItems },
                    multiSelect: function () { return options.multiSelect }
                }
            });
            modalInstance.result.then(function (items) {
                options.callBackFunc(items);
            });
        }
    };
}])


    ///options说明
    ///service:用于查询数据的服务，需要实现Query(queryString)方法
    ///title:弹出窗口的标题
    ///selectedItems:已经选择的项，数组类型，里面的项需要有id、name、type属性
    ///callBackFunc:弹出窗关闭时调用的方法，接收参数为所选择的项的数组
    ///multiSelect:是否允许多选
.factory('selectModalWithType', ["$modal", function ($modal) {
    return {
        open: function (options) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/SelectModalWithType.html?index=' + randomIndex,
                windowClass: 'AddOrgDialog',
                controller: 'SelectWithType',
                backdrop: 'static',
                resolve: {
                    service: function () { return options.service },
                    title: function () { return options.title },
                    selectedItems: function () { return options.selectedItems },
                    multiSelect: function () { return options.multiSelect }
                }
            });
            modalInstance.result.then(function (items) {
                options.callBackFunc(items);
            });
        }
    };
}])

.factory('selectModalWithType', ["$modal", function ($modal) {
    return {
        open: function (options) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/SelectModalWithType.html?index=' + randomIndex,
                windowClass: 'AddOrgDialog',
                controller: 'SelectWithType',
                backdrop: 'static',
                resolve: {
                    service: function () { return options.service },
                    title: function () { return options.title },
                    selectedItems: function () { return options.selectedItems },
                    multiSelect: function () { return options.multiSelect }
                }
            });
            modalInstance.result.then(function (items) {
                options.callBackFunc(items);
            });
        }
    };
}])
.factory('msgModal', ["$modal", function ($modal) {
    return {
        open: function (msg) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/Message.html' ,
                windowClass: 'dialogConfirm',
                controller: 'Message',
                backdrop: 'static',
                resolve: {
                    msg: function () {
                        return msg;
                    }
                }
            });
        }
    };
}])

;//这是结束符，请勿删除。

