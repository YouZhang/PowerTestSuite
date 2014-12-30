//tab显示区域类
//TabZone结构为：
//参数说明：
//id:需要动态创建TabPage的区域id
//activeCSS:激活状态的tab样式
//inactiveCSS:未激活状态的tab样式
//zoneCSS:整个TabZone包含TabPage的样式
function TabZone(id,activeCSS,inactiveCSS,zoneCSS){
//激活时的标签样式类
this.activeCSS = activeCSS;
//未激活时的标签样式类
this.inactiveCSS = inactiveCSS;
//最外层显示区域
this.outerZone = $(id);
this.outerZone.className = zoneCSS;
//动态创建tab及page区域
if(this.outerZone.childElements().length == 0 ||
(this.outerZone.down() && this.outerZone.down().tagName.toLowerCase() != "ul") ||
(this.outerZone.down().next() && this.outerZone.down().next().tagName.toLowerCase() != "div")
){
var frag = document.createDocumentFragment();
var ul = document.createElement("ul");
var div = document.createElement("div");
frag.appendChild(ul);
frag.appendChild(div);
this.outerZone.innerHTML = "";
this.outerZone.appendChild(frag);
}
//内部的tab标签区域
this.innerTabZone = this.outerZone.down();
//内部的显示Pages的区域
this.innerPageZone = this.innerTabZone.next();
//保存生存期内所有添加的TabPage对象
this.tabs = new Array();
}
//向TabZone添加Tab
TabZone.prototype.addTab = function(obj){
this.tabs[this.tabs.length] = obj;
//添加事件监听
var realContext = this;
var focus =this.focus;
//使用Event.observe会使上下文环境发生变化，进而无法直接使用this被指向其他引用
//使用call改变this所指对象
Event.observe(obj.tab, 'click',function(e){focus.call(realContext,obj);});
//为未保护的tab添加关闭事件
if(!obj.protect){
var close = this.close;
Event.observe(obj.tab, 'dblclick',function(e){close.call(realContext,obj);});
}
//添加事件结束
//文档中添加tab及page
this.innerTabZone.appendChild(obj.tab);
this.innerPageZone.appendChild(obj.page);
this.focus(obj);
}
//关闭所有未保护的TabPage
TabZone.prototype.closeAll = function(){
var tabCount = this.tabs.length;
for(var i=this.tabs.length-1;i>=0;i--){
if(!this.tabs[i].protect){
this.innerTabZone.removeChild(this.tabs[i].tab);
this.innerPageZone.removeChild(this.tabs[i].page);
this.tabs.splice(i,1);
}
}
//关闭未保护的tab后处理焦点
if(tabCount > this.tabs.length && this.tabs.length > 0){
this.focus(this.tabs[0]);
}
}
//隐藏除了指定参数的tab
TabZone.prototype.hideExcept = function(obj){
for(var i=0;i0){
this.focus(this.tabs[i]);
}
else if(i > 0){
this.focus(this.tabs[i-1]);
}
return;
}
}
}
}
//tab页类
//name：tab标签名称
//src：page指向的页面地址
//protect：bool，指明tab是否可以被保护，被保护的tab不可被关闭
function TabPage(name,src,protect){
this.protect = protect==true?true:false;
//tab
this.tab = document.createElement("li");
this.tab.innerHTML = name==undefined?"untitled":name;
//page区域
this.page = document.createElement("div");
//page实际内容页面
var iframe = document.createElement("iframe");
iframe.frameBorder = 0;
iframe.src = src==undefined?"":src;
//iframe添加入page区域
this.page.appendChild(iframe);
}

TabZone.prototype.closeTag = function(obj){
        for(var i=0;i<this.tabs.length;i++){
            //判断TAB中的标签名是否和要关闭的标签名称相等（标签名称唯一）

            if(obj.tab.innerHTML.trim() == this.tabs[i].tab.innerHTML.trim()){
                //dom中删除对应tab
                this.innerTabZone.removeChild(this.tabs[i].tab);
                this.innerPageZone.removeChild(this.tabs[i].page);
                
                //tabs集合中删除对应tab对象
                this.tabs.splice(i,1);
                
                //控制关闭tab后焦点行为
                if(i == 0 && this.tabs.length>0){
                    this.focus(this.tabs[i]);
                }
                else if(i > 0){
                    this.focus(this.tabs[i-1]);
                }
                return;
            }
        }

}