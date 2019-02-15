controllers.controller('segmentManagementCtrl', ["$scope", "ipService", "$modal", "loading", "errorModal", "confirmModal","msgModal", function ($scope, ipService, $modal, loading, errorModal, confirmModal,msgModal) {
    $scope.ip_list = [];
    $scope.filterObj = {
        business: "",
        ip: "",
        created_by: "",
        ip_pools: "",
        admin: "",
        work_order: ""
    };
    $scope.pool_list = [];

    $scope.searchList = function () {
        loading.open();
        ipService.search_used_ips({}, $scope.filterObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.ip_list = res.data;
                $scope.pool_list = res.pool_list;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                // if (window.location.href.indexOf("#/segmentManagement") > -1)
                //     setTimeout($scope.searchList, 3000);
            } else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.searchList();
    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;
    $scope.pagingOptions = {
        pageSizes: [5, 10, 25, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.ip_list ? $scope.ip_list : [], pageSize, page);
    };
    $scope.setPagingData = function (data, pageSize, page) {
        $scope.Pagingdata = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };

    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);
    $scope.gridOption = {
        data: "Pagingdata",
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: "ip_pool_name", displayName: "资源池"},
            {field: "start_ip", displayName: "IP地址"},
            {field: "mask", displayName: "掩码"},
            {field: "gateway", displayName: "网关"},
            {
                field: "is_used",
                displayName: "使用状态",
                cellTemplate: '<div ng-if="row.entity.is_used" style="padding-left: 5px;">使用中</div>'
            },
            {field: "business", displayName: "业务系统"},
            {field: "owner", displayName: "管理员"},
            {field: "work_order", displayName: "工单号"},
            {
                displayName: "操作", width: 150,
                cellTemplate: '<div style="display: flex;justify-content: center;align-items: center">' +
                // '<span class="label label-primary label-sm label-btn" ng-click="detailItem(row.entity)">详情</span>&nbsp;' +
                '<span style="margin-left: 10px;padding-top:5px;padding-bottom: 5px;" class="label label-info label-sm label-btn" ng-click="modifyItem(row)">编辑</span>' +
                '<span style="margin-left: 10px;padding-top:5px;padding-bottom: 5px;" class="label label-danger label-sm label-btn" ng-click="recycle(row)">回收</span>' +
                // '<span class="label label-danger label-sm label-btn" ng-click="deleteItem(row)">删除</span>' +
                '</div>'
            }
        ]
    };

    $scope.down_cvs = function () {
        var url = "down_used_ips?" + "ip=" + $scope.filterObj.ip + '&ip_pools=' + $scope.filterObj.ip_pools
            + '&business=' + $scope.filterObj.business + "&admin=" + $scope.filterObj.admin + "&work_order=" + $scope.filterObj.work_order;
        window.open(url);
    };

    // $scope.addIPs = function () {
    //     var modalInstance = $modal.open({
    //         templateUrl: static_url + 'client/views/ipManagement/addIPs.html',
    //         windowClass: 'applyDialog',
    //         controller: 'addIPsCtrl',
    //         backdrop: 'static'
    //     });
    //     modalInstance.result.then(function () {
    //         $scope.searchList();
    //     });
    // };
    //
    $scope.modifyItem = function (row) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/ipManagement/IPmodify.html',
            windowClass: 'dialog_custom',
            controller: 'IPmodifyCtrl',
            backdrop: 'static',
            resolve: {
                itemObj: function () {
                    return angular.copy(row.entity);
                }
            }
        });
        modalInstance.result.then(function () {
            $scope.searchList();
        })
    };

    $scope.sync_cmdb = function () {
        loading.open();
        ipService.sync_cmdb({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.searchList();
            } else {
                errorModal.open(res.data)
            }
        })
    };
    //回收ip
    $scope.recycle = function (row) {
        confirmModal.open({
            text: '是否回收该IP？',
            confirmClick: function () {
                ipService.recycle_ip({}, {param:row.entity}, function (res) {
                    if (res.result) {
                        msgModal.open('回收成功！');
                        $scope.searchList();
                    } else {
                        errorModal.open(['出现异常！']);
                    }
                })
            }
        })
    }
    //导入已用ip
    $scope.uploadCsv = function () {
        CWApp.uploadCsv("uploadFile", callBack);
        $scope.searchList();
    };
    var callBack = function () {
        var content = fr.result;
        content = content.replace(new RegExp("\"", "gm"), "");
        var temp_list = [];
        var content_list = content.substring(0, content.lastIndexOf("\n")).split("\n");
        var column_len = content_list[0].split(",").length;
        var one_errors = [];
        var up_cvs = function (data) {
            console.log(data);
            loading.open();
            ipService.upload_usedIps({}, data, function (res) {
                loading.close()
                if (res.result&&!res.part) {
                    msgModal.open('上传成功！');
                    $scope.searchList();
                }else if(res.result&&res.part){
                    var info = '';
                    for (var i=0;i<res.data.length;i++){
                        info+=res.data[i]+'\n/\n';
                    };
                    msgModal.open(info+'无对应资源池，导入失败！');
                    $scope.searchList();

                }
                else {
                    errorModal.open([res.data]);
                }
            })
        };
        for (var i = 1; i < content_list.length; i++) {
            var device_obj = {};
            var columns = content_list[i].replace("\r", "").split(",");
            console.log('column');
            console.log(columns);
            if (columns.length != column_len)
                continue;
            var device_obj = {
                ip: columns[0],
                mask: columns[1],
                gateway: columns[2],
                is_used:columns[3],
                business:columns[4],
                owner:columns[5],
                work_order:columns[6]
            };
            temp_list.push(device_obj)
        }
        $scope.csvList = temp_list;
        up_cvs($scope.csvList)
    };
    //
    // $scope.deleteItem = function (row) {
    //     confirmModal.open({
    //         text: "请确认是否删除该网段",
    //         confirmClick: function () {
    //             ipService.delete_ips({
    //                 id: row.entity.id
    //             }, {}, function (res) {
    //                 if (res.result) {
    //                     $scope.ip_list.splice(row.rowIndex, 1);
    //                     $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    //                 }
    //                 else {
    //                     errorModal.open(res.data);
    //                 }
    //             })
    //         }
    //     })
    // };
    // $scope.isShowDetail = false;
    // $scope.selectItem = {};
    // $scope.detailItem = function (rowEntity) {
    //     $scope.selectItem = rowEntity;
    //     $scope.isShowDetail = true;
    //
    // };
    // $scope.returnBack = function () {
    //     $scope.isShowDetail = false;
    //
    // }
}]);