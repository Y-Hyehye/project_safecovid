package com.example.project.ui.detail;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.lifecycle.ViewModelProviders;

import com.example.project.MainActivity;
import com.example.project.R;
import com.example.project.ui.detail.region.ChungBuk;
import com.example.project.ui.detail.region.ChungNam;
import com.example.project.ui.detail.region.Gyeounggi;
import com.example.project.ui.detail.region.JeJu;
import com.example.project.ui.detail.region.JeonBuk;
import com.example.project.ui.detail.region.JeonNam;
import com.example.project.ui.detail.region.KangWon;
import com.example.project.ui.detail.region.KyeoungBuk;
import com.example.project.ui.detail.region.KyeoungNam;
import com.example.project.ui.detail.region.Seoul;

public class DetailFragment extends Fragment {

    private DetailViewModel DetailViewModel;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        DetailViewModel =
                ViewModelProviders.of(this).get(DetailViewModel.class);
        View root = inflater.inflate(R.layout.fragment_detail, container, false);

        // 텍스트뷰 리소스 아이디 가져오기
        TextView g_seoulBtn = root.findViewById(R.id.g_btnSeoul);
        TextView g_chungbukBtn = root.findViewById(R.id.g_btnChungBuk);
        TextView g_chungnamBtn = root.findViewById(R.id.g_btnChungNam);
        TextView g_ggBtn = root.findViewById(R.id.g_btnGG);
        TextView g_jejuBtn = root.findViewById(R.id.g_btnJeJu);
        TextView g_jeonbukBtn = root.findViewById(R.id.g_btnJeonBuk);
        TextView g_jeonnamBtn = root.findViewById(R.id.g_btnJeonNam);
        TextView g_kyeoungbukBtn = root.findViewById(R.id.g_btnKyeoungBuk);
        TextView g_kyeoungnamBtn = root.findViewById(R.id.g_btnKyeoungNam);
        TextView g_kangwonBtn = root.findViewById(R.id.g_btnKangWon);

        // OnClickListener를 사용해 서울 텍스트뷰가 눌리면 서울 코로나 상세 정보 프레그먼트로 교체
        g_seoulBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new Seoul()).addToBackStack("Seoul_").commit();
            }
        });

        // OnClickListener를 사용해 충북 텍스트뷰가 눌리면 충북 코로나 상세 정보 프레그먼트로 교체
        g_chungbukBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new ChungBuk()).addToBackStack("ChungBuk_").commit();
            }
        });

        // OnClickListener를 사용해 충남 텍스트뷰가 눌리면 충남 코로나 상세 정보 프레그먼트로 교체
        g_chungnamBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new ChungNam()).addToBackStack("ChungNam_").commit();
            }
        });

        // OnClickListener를 사용해 경기 텍스트뷰가 눌리면 경기 코로나 상세 정보 프레그먼트로 교체
        g_ggBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new Gyeounggi()).addToBackStack("Gyeounggi_").commit();
            }
        });

        // OnClickListener를 사용해 제주 텍스트뷰가 눌리면 제주 코로나 상세 정보 프레그먼트로 교체
        g_jejuBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new JeJu()).addToBackStack("JeJu_").commit();
            }
        });

        // OnClickListener를 사용해 전북 텍스트뷰가 눌리면 전북 코로나 상세 정보 프레그먼트로 교체
        g_jeonbukBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new JeonBuk()).addToBackStack("JeJu_").commit();
            }
        });

        // OnClickListener를 사용해 전남 텍스트뷰가 눌리면 전남 코로나 상세 정보 프레그먼트로 교체
        g_jeonnamBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new JeonNam()).addToBackStack("JeonNam_").commit();
            }
        });

        // OnClickListener를 사용해 경북 텍스트뷰가 눌리면 경북 코로나 상세 정보 프레그먼트로 교체
        g_kyeoungbukBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new KyeoungBuk()).addToBackStack("KyeoungBuk_").commit();
            }
        });

        // OnClickListener를 사용해 경남 텍스트뷰가 눌리면 경남 코로나 상세 정보 프레그먼트로 교체
        g_kyeoungnamBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new KyeoungNam()).addToBackStack("KyeoungNam_").commit();
            }
        });

        // OnClickListener를 사용해 강원 텍스트뷰가 눌리면 강원 코로나 상세 정보 프레그먼트로 교체
        g_kangwonBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.notifications_frame, new KangWon()).addToBackStack("KangWon_").commit();
            }
        });
        return root;
    }
    // 액션바 타이틀 변경
    public void onResume() {
        super.onResume();
        FragmentActivity activity = getActivity();
        ((MainActivity) activity).setActionBarTitle("지역별 코로나 정보");
    }
}