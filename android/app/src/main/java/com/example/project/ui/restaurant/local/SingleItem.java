package com.example.project.ui.restaurant.local;

// 데이터 보관 클래스
public class SingleItem {
    public String nameStr;
    public String addressStr;
    public String numberStr;
    public String typeStr;

    // 이름, 주소, 번호, 업종에 대한 생성자
    public SingleItem(String name, String address, String number, String type) {
        this.nameStr = name;
        this.addressStr = address;
        this.numberStr = number;
        this.typeStr = type;
    }

    // 데이터를 받고 쓰기 위한 setter 및 getter
    public void setName(String name) {
        nameStr = name;
    }
    public void setAddress(String address) {
        addressStr = address;
    }
    public void setNumber(String number) {
        numberStr = number;
    }
    public void setType(String type) {
        typeStr = type;
    }
    public String getName() {
        return this.nameStr;
    }
    public String getAddress() {
        return this.addressStr;
    }
    public String getNumber() {
        return this.numberStr;
    }
    public String getType() {
        return this.typeStr;
    }
}
