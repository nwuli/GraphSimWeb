$(function () {
    $.get('/graph', function (result) {//jquery中发送一个http请求获取json数据
        /*var style = [
          { selector: 'node[label = "Person"]', css: {'background-color': '#6FB1FC','content': 'data(name)'}},
          { selector: 'node[label = "Movie"]', css: {'background-color': '#F5A45D','content': 'data(title)'}},
           { selector: 'edge', css: {'curve-style': 'bezier','target-arrow-shape': 'triangle', 'content': 'data(relationship)'}}
        ];*/

        //将cytoscape样式定义为变量cy
        var cy = window.cy = cytoscape({
            container: document.getElementById('left'),	  // 定义需要渲染的容器
            /*style: style,*/
            style: cytoscape.stylesheet()
                .selector('node[nodeType="node"]').css({'background-color': '#6FB1FC', 'content': 'node'}) //节点样式
                .selector('node[nodeType="method"]').css({'background-color': '#F5A45D', 'content': 'method'})
                .selector('edge').css({
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'line-color': '#ffaaaa',
                    'target-arrow-color': '#ffaaaa',
                    'content': 'data(relationship)'
                }) //边线样式
                .selector(':selected').css({
                    'background-color': 'black',
                    'line-color': 'black',
                    'target-arrow-color': 'black',
                    'source-arrow-color': 'black',
                    'opacity': 1
                }) //点击后节点与边的样式
                .selector('.faded').css({'opacity': 0.25, 'text-opacity': 0})
                .selector('node[nodeType="file"]').css({'background-color': '#ffaaaa', 'content': 'file'}),
            layout: {name: 'cose', fit: true},  //画布自适应大小
            elements: result.elements//get请求的数据为result，注意前台页面传过来的数据格式
        });
        /* cy.nodes().forEach(function(ele) {
            ele.qtip({
                content: {
                text: function(ele){return 'Example qTip on ele ' + ele.data('id')},
                title: ele.data('name')
                },
                style: {
                classes: 'qtip-bootstrap'
                },
                position: {
                my: 'bottom center',
                at: 'top center',
                }

            })
        }); */

        // cy.elements().qtip({ //点击elements处的提醒
        //     content: //function(){ return 'Example qTip on ele ' + this.id() },
        //         {
        //             text: 'info',
        //             title: function () {
        //                 return 'Attribute :' + this.
        //             }
        //         },
        //     position: {
        //         my: 'top center',
        //         at: 'bottom center'
        //     },
        //     style: {
        //         classes: 'qtip-bootstrap',
        //         tip: {
        //             width: 16,
        //             height: 8
        //         }
        //     }
        // });

        // call on core,点击空白处的提醒
        cy.qtip({
            content: 'Example qTip on core bg',
            position: {
                my: 'top center',
                at: 'bottom center'
            },
            show: {
                cyBgOnly: true
            },
            style: {
                classes: 'qtip-bootstrap',
                tip: {
                    width: 16,
                    height: 8
                }
            }
        });

        cy.nodes().forEach(function (ele) {
            ele.qtip({
                content: {
                    text: qtipText(ele),
                    title: ele.data('fileName')
                },
                style: {
                    classes: 'qtip-bootstrap',
                    tip: {
                        width: 60,
                        height: 20
                    }
                },
                position: {
                    my: 'bottom center',
                    at: 'top center',
                    target: ele
                }
            })
        });

        function qtipText(node) {
            var description = '<i>' + "Id:" + node.data('id') + '<br>' + "Version:" + node.data('version') + '</i>';
            return description + '</p>';
        }


    }, 'json');
});

function Parse() {//点击按钮触发函数
    //将cytoscape样式定义为变量cy
    $.get('/Parse', function (result) {
        var ty = window.cy = cytoscape({
            container: document.getElementById('right'),	  // 定义需要渲染的容器
            /*style: style,*/
            style: cytoscape.stylesheet()
                .selector('node[nodeType="change"]').css({'background-color': '#F51D10', 'content': 'node'})
                .selector('node[nodeType="node"]').css({'background-color': '#6FB1FC', 'content': 'node'}) //节点样式
                .selector('node[nodeType="method"]').css({'background-color': '#F5A45D', 'content': 'method'})
                .selector('edge').css({
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'line-color': '#ffaaaa',
                    'target-arrow-color': '#ffaaaa',
                    'content': 'data(relationship)'
                }) //边线样式
                .selector(':selected').css({
                    'background-color': 'black',
                    'line-color': 'black',
                    'target-arrow-color': 'black',
                    'source-arrow-color': 'black',
                    'opacity': 1
                }) //点击后节点与边的样式
                .selector('.faded').css({'opacity': 0.25, 'text-opacity': 0})
                .selector('node[nodeType="file"]').css({'background-color': '#ffaaaa', 'content': 'file'}),
            layout: {name: 'cose', fit: true},  //画布自适应大小
            elements: result.elements//get请求的数据为result，注意前台页面传过来的数据格式
        });
    }, 'json')
}

