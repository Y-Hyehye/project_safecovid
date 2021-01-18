package com.example.project.ui.restaurant.local;

import android.os.Build;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.lifecycle.ViewModelProviders;

import com.example.project.MainActivity;
import com.example.project.R;
import com.example.project.ui.restaurant.local.ChungBuk.ChungBukFragment;
import com.example.project.ui.restaurant.local.ChungNam.ChungNamFragment;
import com.example.project.ui.restaurant.local.Gyeounggi.GyeonggiFragment;
import com.example.project.ui.restaurant.local.JeJu.JeJuFragment;
import com.example.project.ui.restaurant.local.JeonBuk.JeonBukFragment;
import com.example.project.ui.restaurant.local.JeonNam.JeonNamFragment;
import com.example.project.ui.restaurant.local.KangWon.KangWonFragment;
import com.example.project.ui.restaurant.local.KyeoungBuk.KyeoungBukFragment;
import com.example.project.ui.restaurant.local.KyeoungNam.KyeoungNamFragment;
import com.example.project.ui.restaurant.local.Seoul.SeoulFragment;

public class LocalSelectFragment extends Fragment {
    SeoulFragment seoulFragment;
    GyeonggiFragment gyeonggiFragment;

    private LocalSelectViewModel localSelectViewModel;


    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        localSelectViewModel =
                ViewModelProviders.of(this).get(LocalSelectViewModel.class);
        View root = inflater.inflate(R.layout.fragment_localselect, container, false);

        ImageView seoulBtn = root.findViewById(R.id.btnSeoul);
        ImageView gyeonggiBtn = root.findViewById(R.id.btnGG);
        ImageView chungnamBtn = root.findViewById(R.id.btnChungNam);
        ImageView chungbukBtn = root.findViewById(R.id.btnChungBuk);
        ImageView jeonnamBtn = root.findViewById(R.id.btnJeonNam);
        ImageView jeonbukBtn = root.findViewById(R.id.btnJeonBuk);
        ImageView kyeoungnamBtn = root.findViewById(R.id.btnKyeoungNam);
        ImageView kyeoungbukBtn = root.findViewById(R.id.btnKyeoungBuk);
        ImageView kangwonBtn = root.findViewById(R.id.btnKangWon);
        ImageView jejuBtn = root.findViewById(R.id.btnJeJu);


        seoulBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                    getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new SeoulFragment()).addToBackStack("Seoul").commit();
            }
        });

        gyeonggiBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                    getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new GyeonggiFragment()).addToBackStack("GG").commit();
            }
        });

        chungnamBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new ChungNamFragment()).addToBackStack("GG").commit();
            }
        });

        chungbukBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new ChungBukFragment()).addToBackStack("GG").commit();
            }
        });

        jeonnamBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new JeonNamFragment()).addToBackStack("GG").commit();
            }
        });

        jeonbukBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new JeonBukFragment()).addToBackStack("GG").commit();
            }
        });

        kyeoungnamBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new KyeoungNamFragment()).addToBackStack("GG").commit();
            }
        });

        kyeoungbukBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new KyeoungBukFragment()).addToBackStack("GG").commit();
            }
        });

        kangwonBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new KangWonFragment()).addToBackStack("GG").commit();
            }
        });

        jejuBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getChildFragmentManager().beginTransaction().replace(R.id.Local_Select_Frame, new JeJuFragment()).addToBackStack("GG").commit();
            }
        });


        return root;
    }
    // 액션바 타이틀 변경
    public void onResume() {
        super.onResume();
        FragmentActivity activity = getActivity();
        ((MainActivity) activity).setActionBarTitle("안심 식당");
    }
}