package com.example.project.ui.detail.region;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.lifecycle.ViewModelProviders;

import com.example.project.MainActivity;
import com.example.project.R;
import com.example.project.ui.detail.DetailViewModel;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.squareup.picasso.Picasso;


public class Seoul extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    private static final String TAG = "SeoulFragment";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private DetailViewModel DetailViewModel;

    // DatabaseReference 선언
    private DatabaseReference reference;

    // 이미지뷰 변수 선언
    ImageView image1, image2;

    // 텍스트뷰 변수 선언
    TextView text1, text2, text3;

    public Seoul() {

    }
    // 서울 생성자
    public static Seoul newInstance(String param1, String param2) {
        Seoul fragment = new Seoul();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        DetailViewModel =
                ViewModelProviders.of(this).get(DetailViewModel.class);
        View root = inflater.inflate(R.layout.graph_seoul, container, false);

        // 이미지뷰, 텍스트뷰 리소스 아이디 가져오기
        image1 = (ImageView) root.findViewById(R.id.s_img1);
        image2 = (ImageView) root.findViewById(R.id.s_img2);

        text1 = (TextView) root.findViewById(R.id.s_table_t1);
        text2 = (TextView) root.findViewById(R.id.s_table_t2);
        text3 = (TextView) root.findViewById(R.id.s_table_t3);


        // DatabaseReference 인스턴스 가져오기
        reference = FirebaseDatabase.getInstance().getReference();

        // Iamges(자식노드) 위치에 접근
        Query query = reference.child("Images");

        // local(자식노드) 위치에 접근
        Query query_data = reference.child("local");

        query.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                // 그래프 사진 url 불러오기
                String s_url1 = dataSnapshot.child("seoul/url1").getValue().toString();
                String s_url2 = dataSnapshot.child("seoul/url2").getValue().toString();

                // 그래프 사진 url을 사용해 이미지뷰에 그래프 사진 넣기
                if(!s_url1.isEmpty()) {
                    Picasso.get()
                            .load(s_url1)
                            .into(image1);

                }
                if(!s_url2.isEmpty()) {
                    Picasso.get()
                            .load(s_url2)
                            .into(image2);
                }
            }
            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
            }
        });

        query_data.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                // 확진자수, 지역발생수, 해외유입수 데이터 불러오기
                String decide  = dataSnapshot.child("seoul/decide").getValue().toString();
                String local_decide = dataSnapshot.child("seoul/local_decide").getValue().toString();
                String overflow_decide = dataSnapshot.child("seoul/overflow_decide").getValue().toString();

                // 텍스트뷰에 각 데이터 넣기
                text1.setText(decide);
                text2.setText(local_decide);
                text3.setText(overflow_decide);
            }
            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
            }
        });

        return root;
    }
    // 액션바 타이틀 변경
    public void onResume() {
        super.onResume();
        FragmentActivity activity = getActivity();
        ((MainActivity) activity).setActionBarTitle("서울");
    }
}
