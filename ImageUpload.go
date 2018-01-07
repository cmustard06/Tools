package main

import(
	"io"
	"net/http"
	"log"
	"fmt"
	"os"
	"io/ioutil"
)

//将路径设置为常量,注意golang的项目环境，否则路径会设置错误

const UPLOAD_DIR  = `./uploads`

func uploadHandler(w http.ResponseWriter,r *http.Request){
	if r.Method == "GET"{ //使用get方法请求upload路径，返回的网页内容
		io.WriteString(w,`<html><body><form method="POST" action="/upload"`+` enctype="multipart/form-data">`+`Choose an image to upload:<input name="image" type="file"/>`+`<input type="submit" value="上传"/>`+`</form></body></html>`)
		return
	}
	//处理post请求
	if r.Method == "POST"{
		f,h,err := r.FormFile("image")   //multipart.File, *multipart.FileHeader, error
		if err != nil{
			http.Error(w,err.Error(),http.StatusInternalServerError)  //将错误发给response在网页中回显
			return
		}
		//获取文件
		filename := h.Filename  //获取文件名
		defer f.Close()
		//本地创建文件存储图片
		t,err := os.Create(UPLOAD_DIR+"/"+filename)
		if err!=nil{
			http.Error(w,err.Error(),http.StatusInternalServerError)
			return
		}
		defer t.Close()
		if _,err:=io.Copy(t,f);err!=nil{
			http.Error(w,err.Error(),http.StatusInternalServerError)
			return
		}
		//将网页重定向到/view
		http.Redirect(w,r,"/view?id="+filename,http.StatusFound)
	}

}

func viewHandler(w http.ResponseWriter,r *http.Request){
	imageId := r.FormValue("id") //获取get参数id的值
	imagePath := UPLOAD_DIR+"/"+imageId
	//处理不存在的图片
	if exists := isExists(imagePath);!exists{
		http.NotFound(w,r)
		return
	}
	//设置header头部的值
	w.Header().Set("Content-Type","image")
	//回应客户端的请求
	http.ServeFile(w,r,imagePath)
}
//处理不存在的图片
func isExists(path string) bool{
	_,err:=os.Stat(path)
	if err==nil{
		return true
	}
	return os.IsExist(err)
}

//列出所有已经上传的图片
func listHandler(w http.ResponseWriter,r *http.Request){
	fileInfoAddr,err:=ioutil.ReadDir(UPLOAD_DIR)
	if err!=nil{
		http.Error(w,err.Error(),http.StatusInternalServerError)
		return
	}
	var listHTML string
	for _,fileInfo := range fileInfoAddr{
		imgid := fileInfo.Name()
		listHTML +=`<html><body><li><<a href="/view?id=`+imgid+`">`+imgid+`</a></li></body></html>`

	}
	io.WriteString(w,listHTML)
}

func main(){
	cwdDir,_ := os.Getwd()
	fmt.Println(cwdDir)
	http.HandleFunc("/upload",uploadHandler)
	http.HandleFunc("/view",viewHandler)
	http.HandleFunc("/list",listHandler)
	fmt.Println("Starting listen 8088...")
	err := http.ListenAndServe(":8088",nil)
	if err!=nil{
		log.Fatal("ListenAndServe: ",err.Error())
	}
}
