package com.example.project.ui.home;

import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.ViewFlipper;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.lifecycle.ViewModelProviders;

import com.example.project.MainActivity;
import com.example.project.R;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.squareup.picasso.Picasso;

import java.text.SimpleDateFormat;
import java.util.Date;

public class HomeFragment extends Fragment {
    private static final String TAG = "MainActivity";

    private HomeViewModel homeViewModel;

    // 이미지 슬라이더로 출력하기 위한 ViewFlipper 선언
    ViewFlipper v_fllipper;

    // DatabaseReference 선언
    private DatabaseReference reference;

    // 이미지뷰 변수 선언
    ImageView image1, image2, image3;

    // 텍스트뷰 변수 서언
    TextView text1, text2, text3, whenDate;

    // 버튼 변수 선언
    Button b_link;

    // 날짜를 나타내기 위한 포맷 지정
    private SimpleDateFormat mFormat = new SimpleDateFormat("yyyyMM/dd");

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel =
                ViewModelProviders.of(this).get(HomeViewModel.class);
        View root = inflater.inflate(R.layout.fragment_home, container, false);


        // 텍스트뷰 리소스 아이디 가져오기
        whenDate = root.findViewById(R.id.whenDate);

        Date date = new Date(); // 현재 시간을 날짜에 저장
        String time = mFormat.format(date); // string 변수 저장
        whenDate.setText(time); // 현재 날짜로 설정


        // ViewFlipper 리소스 아이디 가져오기
        v_fllipper = root.findViewById(R.id.image_slide);

        // 이미지뷰, 텍스트뷰, 버튼 리소스 아이디 가져오기
        image1 = (ImageView) root.findViewById(R.id.iv1);
        image2 = (ImageView) root.findViewById(R.id.iv2);
        image3 = (ImageView) root.findViewById(R.id.iv3);

        text1 = (TextView) root.findViewById(R.id.t1);
        text2 = (TextView) root.findViewById(R.id.t2);
        text3 = (TextView) root.findViewById(R.id.t3);

        b_link = (Button) root.findViewById(R.id.btn_link);

        // 자동으로 flipping 시작, 2초 간격으로 사진 슬라이드
        v_fllipper.setFlipInterval(2000);
        v_fllipper.setAutoStart(true);

        // DatabaseReference 인스턴스 가져오기
        reference = FirebaseDatabase.getInstance().getReference();

        // Iamges(자식노드) 위치에 접근
        Query query = reference.child("total");

        query.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                // 그래프 사진 url 불러오기
                String url1 = dataSnapshot.child("url1").getValue().toString();
                String url2 = dataSnapshot.child("url2").getValue().toString();
                String url3 = dataSnapshot.child("url3").getValue().toString();

                // 확진자수, 격리해제수, 사망자수 데이터 불러오기
                String decide  = dataSnapshot.child("decide").getValue().toString();
                String clear = dataSnapshot.child("clear").getValue().toString();
                String death = dataSnapshot.child("death").getValue().toString();

                // 텍스트뷰에 각 데이터 넣기
                text1.setText(decide);
                text2.setText(clear);
                text3.setText(death);

                // 그래프 사진 url을 사용해 이미지뷰에 그래프 사진 넣기
                if(!url1.isEmpty()) {
                    Picasso.get()
                            .load(url1)
                            .into(image1);

                }
                if(!url2.isEmpty()) {
                    Picasso.get()
                            .load(url2)
                            .into(image2);
                }
                if(!url3.isEmpty()) {
                    Picasso.get()
                            .load(url3)
                            .into(image3);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
            }
        });

        // OnClickListener를 사용해 버튼이 눌리면 질병관리본부 홈페이지로 넘어가도록 함
        b_link.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("http://www.kdca.go.kr/"));
                startActivity(intent);
            }
        });
        return root;
    }

    // 액션바 타이틀 변경
    public void onResume() {
        super.onResume();
        FragmentActivity activity = getActivity();
        if (activity != null) {
            ((MainActivity) activity).setActionBarTitle("SAFE COVID");
        }
    }
}