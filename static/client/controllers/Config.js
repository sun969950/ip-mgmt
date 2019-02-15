//配置信息
var CWApp = {
    HeaderHeight: 66,
    BodyTopBarHeight: 40,
    FooterHeight: 0,
    //base页面高度自适应函数
    InitSiteHeight: function () {
        var winHeight = 0;
        if (window.innerHeight)
            winHeight = window.innerHeight;
        if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
            winHeight = document.documentElement.clientHeight;
        }
        $("#main2").css("height", (winHeight - CWApp.HeaderHeight - CWApp.BodyTopBarHeight - CWApp.FooterHeight - 2) + 'px');
        //$("#main-container").css("height", (winHeight - CWApp.HeaderHeight - CWApp.FooterHeight - 2) + 'px');
        //$("#sidebar_cwLeftMenu").css("min-height", (winHeight - CWApp.HeaderHeight - CWApp.FooterHeight) + 'px');
    },
    //判断是否为IP格式
    isIP: function (ip) {
        if (ip == "" || ip == null)
            return true;
        var pattern = /^[\d\.]+$/i;
        if (!pattern.test(ip))
            return false;
        if (ip.indexOf(".") < 0)
            return false;
        if (ip.split(".").length != 4)
            return false;
        var ipList = ip.split(".");
        for (var i = 0; i < ipList.length; i++) {
            if (ipList[i] > 255 || ipList[i] < 0)
                return false;
        }
        if (ipList[0] == 0)
            return false;
        return true;
    },
    //判断是否为数字
    isNum: function (num) {
        var pattern = /^[\d]+$/i;
        if (!pattern.test(num))
            return false;
        return true;
    },
    //判断是否为正常的日期值
    isDay: function (day) {
        var pattern = /^[\d]+$/i;
        if (!pattern.test(day))
            return false;
        if (day < 0)
            return false;
        if (day > 31)
            return false;
        return true;
    },
    //判断是否为正常的小时值
    isHour: function (hour) {
        var pattern = /^[\d]+$/i;
        if (!pattern.test(hour))
            return false;
        if (hour < 0)
            return false;
        if (hour > 23)
            return false;
        return true;
    },
    //判断是否为正常的分钟值
    isMinute: function (minute) {
        var pattern = /^[\d]+$/i;
        if (!pattern.test(minute))
            return false;
        if (minute < 0)
            return false;
        if (minute > 59)
            return false;
        return true;
    },
    isMail: function (mail) {
        if (mail.split("@").length != 2) {
            return false;
        }
        dns = mail.split("@")[1];
        var pattern = /^[a-z\A-Z\d\.]+$/i;
        if (!pattern.test(dns)) {
            return false;
        }
        if (dns.indexOf("..") > -1) {
            return false;
        }
        if (dns[0] == ".") {
            return false;
        }
        if (dns[dns.length - 1] == ".") {
            dns = dns.substring(0, dns.length - 1);
        }
        var lista = dns.split(".");
        if (lista.length < 2) {
            return false
        }
        return true;
    },
    isCData: function (data) {
        var pattern = /^[a-z\A-Z\d\.]+$/i;
        if (!pattern.test(data)) {
            return false;
        }
        if (data[data.length - 1] == ".")
            data = data.substring(0, data.length - 1);
        datas = data.split(".");
        if (datas.length < 2)
            return false;
        for (var i in datas) {
            if (datas[i] == "") {
                return false;
            }
        }
        return true;
    },
    //csv上传功能，可以直接读取csv中的内容
    //upload_id为页面input上传框的ID； callBack 为回调函数，在回调函数中，可以使用fr.result获取值
    uploadCsv: function (upload_id, callBack) {
        if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
            alert('The File APIs are not fully supported in this browser.');
            return;
        }
        input = document.getElementById(upload_id);
        if (!input) {
            alert("Um, couldn't find the fileinput element.");
        }
        else if (!input.files) {
            alert("This browser doesn't seem to support the `files` property of file inputs.");
        }
        else if (!input.files[0]) {
            alert("Please select a file before clicking 'Load'");
        }
        else {
            file = input.files[0];
            fr = new FileReader();
            fr.onload = callBack;
            fr.readAsText(file, "gb2312");
            // fr.readAsDataURL(file);
        }
    },
    ValidateDate: function (t, date_str) {
        var now_time = t('date')(new Date(), 'yyyy-MM-dd HH:mm:ss');
        var select_time = new Date(date_str);
        if (select_time == "Invalid Date") {
            return "不是合理的时间格式";
        }
        var select_time = t('date')(new Date(date_str), 'yyyy-MM-dd HH:mm:ss');
        if (select_time <= now_time) {
            return "所选时间比当前时间小";
        }
        return "";
    },
    isDNS: function (dns) {
        var pattern = /^[a-z\A-Z\d\.]+$/i;
        if (!pattern.test(dns)) {
            return false;
        }
        if (dns.indexOf("..") > -1) {
            return false;
        }
        if (dns[0] == ".") {
            return false;
        }
        if (dns[dns.length - 1] == ".") {
            dns = dns.substring(0, dns.length - 1);
        }
        var lista = dns.split(".");
        if (lista.length < 2) {
            return false
        }
        return true;
    },
    isEng: function (data) {
        var pattern = /^[a-z\A-Z\0-9\d\.\-\_\;]+$/i;
        if (data == "") {
            return false;
        }
        return pattern.test(data)

    }
};
