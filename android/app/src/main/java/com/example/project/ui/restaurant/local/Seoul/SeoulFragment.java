package com.example.project.ui.restaurant.local.Seoul;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;

import com.example.project.MainActivity;
import com.example.project.R;

public class SeoulFragment extends Fragment {

    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.local_seoul, container, false);

        setHasOptionsMenu(true);    // 액티비티보다 프레그먼트 메뉴를 우선시 하기 위함

        getChildFragmentManager().beginTransaction().replace(R.id.fragmentSeoul, new Map()).addToBackStack("Map").commit(); // 서울 안심 식당 맵 프레그먼트로 교체

        return root;
    }

    // 메뉴 생성
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        inflater.inflate(R.menu.menu, menu) ;
    }

    // 메뉴 이벤트 설정
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.btn_map:
                goMap();
                return true;
            case R.id.btn_list:
                goList();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    // 서울 맵 프레그먼트로 교체
    public void goMap(){
        getChildFragmentManager().beginTransaction().replace(R.id.fragmentSeoul, new Map()).addToBackStack("Map").commit();
    }

    // 서울 리스트 프레그먼트로 교체
    public void goList(){
        getChildFragmentManager().beginTransaction().replace(R.id.fragmentSeoul, new List()).addToBackStack("List").commit();
    }

    // 액션바 타이틀 변경
    public void onResume() {
        super.onResume();
        FragmentActivity activity = getActivity();
        if (activity != null) {
            ((MainActivity) activity).setActionBarTitle("서울");
        }
    }
}