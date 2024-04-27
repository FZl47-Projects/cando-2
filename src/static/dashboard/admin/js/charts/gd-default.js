"use strict";

!function (NioApp, $) {
    "use strict";

    //////// for developer - User Balance ////////
    // Avilable options to pass from outside
    // labels: array,
    // legend: false - boolean,
    // dataUnit: string, (Used in tooltip or other section for display)
    // datasets: [{label : string, color: string (color code with # or other format), data: array}]
    let order_value = []
    try {
        let order_chart_data = JSON.parse(document.getElementById('salesRevenue').getAttribute('data-chart'))
        for (let chart_data of order_chart_data) {
            order_value.push(chart_data.total)
        }
    } catch (e) {
    }
    var salesRevenue = {
        labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
        dataUnit: 'سفارش',
        stacked: true,
        datasets: [{
            label: "درآمد فروش",
            color: [NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), "#6576ff"],
            data: order_value
        }]
    };
    var activeSubscription = {
        labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور"],
        dataUnit: 'تومان',
        stacked: true,
        datasets: [{
            label: "کاربر فعال",
            color: [NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), "#6576ff"],
            data: [8200, 7800, 9500, 5500, 9200, 9690]
        }]
    };
    var totalSubscription = {
        labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور"],
        dataUnit: 'تومان',
        stacked: true,
        datasets: [{
            label: "کاربر فعال",
            color: [NioApp.hexRGB("#aea1ff", .2), NioApp.hexRGB("#aea1ff", .2), NioApp.hexRGB("#aea1ff", .2), NioApp.hexRGB("#aea1ff", .2), NioApp.hexRGB("#aea1ff", .2), "#aea1ff"],
            data: [8200, 7800, 9500, 5500, 9200, 9690]
        }]
    };

    function salesBarChart(selector, set_data) {
        var $selector = selector ? $(selector) : $('.sales-bar-chart');
        $selector.each(function () {
            var $self = $(this),
                _self_id = $self.attr('id'),
                _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data,
                _d_legend = typeof _get_data.legend === 'undefined' ? false : _get_data.legend;
            var selectCanvas = document.getElementById(_self_id).getContext("2d");
            var chart_data = [];
            for (var i = 0; i < _get_data.datasets.length; i++) {
                chart_data.push({
                    label: _get_data.datasets[i].label,
                    data: _get_data.datasets[i].data,
                    // Styles
                    backgroundColor: _get_data.datasets[i].color,
                    borderWidth: 2,
                    borderColor: 'transparent',
                    hoverBorderColor: 'transparent',
                    borderSkipped: 'bottom',
                    barPercentage: .7,
                    categoryPercentage: .7
                });
            }
            var chart = new Chart(selectCanvas, {
                type: 'bar',
                data: {
                    labels: _get_data.labels,
                    datasets: chart_data
                },
                options: {
                    plugins: {
                        legend: {
                            display: _get_data.legend ? _get_data.legend : false,
                            rtl: NioApp.State.isRTL,
                            labels: {
                                boxWidth: 30,
                                padding: 20,
                                color: '#6783b8'
                            }
                        },
                        tooltip: {
                            enabled: true,
                            rtl: NioApp.State.isRTL,
                            callbacks: {
                                // title: function title() {
                                //     return false;
                                // },
                                label: function label(context) {
                                    return "".concat(context.parsed.y, " ").concat(_get_data.dataUnit);
                                }
                            },
                            backgroundColor: '#1c2b46',
                            titleFont: {
                                size: 13
                            },
                            titleColor: '#fff',
                            titleMarginBottom: 4,
                            bodyColor: '#fff',
                            bodyFont: {
                                size: 12
                            },
                            bodySpacing: 10,
                            padding: 12,
                            footerMarginTop: 0,
                            displayColors: false
                        }
                    },
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            display: false,
                            stacked: _get_data.stacked ? _get_data.stacked : false,
                            ticks: {
                                beginAtZero: true
                            }
                        },
                        x: {
                            display: false,
                            stacked: _get_data.stacked ? _get_data.stacked : false,
                            ticks: {
                                reverse: NioApp.State.isRTL
                            }
                        }
                    }
                }
            });
        });
    }

    // init chart
    NioApp.coms.docReady.push(function () {
        salesBarChart();
    });
    let sale_label = []
    let sale_value = []
    try {
        let sale_chart_data = JSON.parse(document.getElementById('salesOverview').getAttribute('data-chart'))
        for (let chart_data of sale_chart_data) {
            sale_label.push(chart_data.day)
            sale_value.push(chart_data.total_amount)
        }
    } catch (e) {
    }
    var salesOverview = {
        labels: sale_label,
        dataUnit: 'تومان',
        lineTension: 0.4,
        datasets: [{
            label: "نمای کلی فروش",
            color: "#798bff",
            background: NioApp.hexRGB('#798bff', .35),
            data: sale_value
        }]
    };

    function lineSalesOverview(selector, set_data) {
        var $selector = selector ? $(selector) : $('.sales-overview-chart');
        $selector.each(function () {
            var $self = $(this),
                _self_id = $self.attr('id'),
                _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data;
            var selectCanvas = document.getElementById(_self_id).getContext("2d");
            var chart_data = [];
            for (var i = 0; i < _get_data.datasets.length; i++) {
                chart_data.push({
                    label: _get_data.datasets[i].label,
                    tension: _get_data.lineTension,
                    backgroundColor: _get_data.datasets[i].background,
                    fill: true,
                    borderWidth: 4,
                    borderColor: _get_data.datasets[i].color,
                    pointBorderColor: "transparent",
                    pointBackgroundColor: "transparent",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: _get_data.datasets[i].color,
                    pointBorderWidth: 4,
                    pointHoverRadius: 6,
                    pointHoverBorderWidth: 4,
                    pointRadius: 6,
                    pointHitRadius: 6,
                    data: _get_data.datasets[i].data
                });
            }
            var chart = new Chart(selectCanvas, {
                type: 'line',
                data: {
                    labels: _get_data.labels,
                    datasets: chart_data
                },
                options: {
                    plugins: {
                        legend: {
                            display: _get_data.legend ? _get_data.legend : false,
                            rtl: NioApp.State.isRTL,
                            labels: {
                                boxWidth: 30,
                                padding: 20,
                                color: '#6783b8'
                            }
                        },
                        tooltip: {
                            enabled: true,
                            rtl: NioApp.State.isRTL,
                            callbacks: {
                                label: function label(context) {
                                    return "".concat(numberWithCommas(context.parsed.y), " ").concat(_get_data.dataUnit);
                                }
                            },
                            backgroundColor: '#1c2b46',
                            titleFont: {
                                size: 13
                            },
                            titleColor: '#fff',
                            titleMarginBottom: 4,
                            bodyColor: '#fff',
                            bodyFont: {
                                size: 12
                            },
                            bodySpacing: 10,
                            padding: 12,
                            footerMarginTop: 0,
                            displayColors: false
                        }
                    },
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            display: true,
                            stacked: _get_data.stacked ? _get_data.stacked : false,
                            position: NioApp.State.isRTL ? "right" : "left",
                            ticks: {
                                beginAtZero: true,
                                font: {
                                    size: 11
                                },
                                color: '#9eaecf',
                                padding: 10,
                                callback: function callback(value, index, values) {
                                    return numberWithCommas(value) + ' تومان';
                                },
                                min: 100,
                                stepSize: 3000
                            },
                            grid: {
                                color: NioApp.hexRGB("#526484", .2),
                                tickLength: 0,
                                zeroLineColor: NioApp.hexRGB("#526484", .2),
                                drawTicks: false
                            }
                        },
                        x: {
                            display: true,
                            stacked: _get_data.stacked ? _get_data.stacked : false,
                            ticks: {
                                font: {
                                    size: 9
                                },
                                color: '#9eaecf',
                                source: 'auto',
                                padding: 10,
                                reverse: NioApp.State.isRTL
                            },
                            grid: {
                                color: "transparent",
                                tickLength: 0,
                                zeroLineColor: 'transparent',
                                drawTicks: false
                            }
                        }
                    }
                }
            });
        });
    }

    // init chart
    NioApp.coms.docReady.push(function () {
        lineSalesOverview();
    });
}(NioApp, jQuery);