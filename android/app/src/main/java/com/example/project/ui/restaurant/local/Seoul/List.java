package com.example.project.ui.restaurant.local.Seoul;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.project.MainActivity;
import com.example.project.R;
import com.example.project.ui.restaurant.local.SingleAdapter;
import com.example.project.ui.restaurant.local.SingleItem;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;

public class List extends Fragment {

    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    private String mParam1;
    private String mParam2;

    // RecyclerView 선언
    RecyclerView recyclerView;
    // SingleAdapter 선언
    SingleAdapter adapter;
    // DatabaseReference 선언
    private DatabaseReference reference;

    public List() {
    }

    // 생성자
    public static List newInstance(String param1, String param2) {
        List fragment = new List();
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
        View root = inflater.inflate(R.layout.list_seoul, container, false);

        // RecyclerView 리소스 아이디 가져오기
        recyclerView = root.findViewById(R.id.recyclerView);

        // 레이아웃매니저 객체 생성
        LinearLayoutManager layoutManager = new LinearLayoutManager(getContext());

        //레이아웃매니저 객체를 리사이클러 뷰에 설정
        recyclerView.setLayoutManager(layoutManager);

        // SingleAdapter 객체 생성
        adapter = new SingleAdapter(getContext());

        // DatabaseReference 인스턴스 가져오기
        reference = FirebaseDatabase.getInstance().getReference();

        // restaurant(자식노드) 위치에 접근
        Query query = reference.child("restaurant");

        query.addValueEventListener(new ValueEventListener() {
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                // seoul의 데이터 개수 세기
                int cnt = (int)dataSnapshot.child("seoul").getChildrenCount();
                final String[] name = new String[cnt];
                final String[] address = new String[cnt];
                final String[] number = new String[cnt];
                final String[] type = new String[cnt];

                // 서울 내의 안심식당 사업장명, 주소, 전화번호, 업종상세 데이터 가져오기
                for(int idx = 0; idx < cnt; idx++){
                    name[idx] = dataSnapshot.child("seoul").child(String.valueOf(idx)).child("사업장명").getValue(String.class);
                    address[idx] = dataSnapshot.child("seoul").child(String.valueOf(idx)).child("주소").getValue(String.class);
                    number[idx] = dataSnapshot.child("seoul").child(String.valueOf(idx)).child("전화번호").getValue(String.class);
                    type[idx] = dataSnapshot.child("seoul").child(String.valueOf(idx)).child("업종상세").getValue(String.class);
                }

                // 아이템 추가, 어댑터에 연결
                for(int i = 0; i < cnt; i++){
                    adapter.addItem(new SingleItem(name[i], address[i], number[i], type[i]));
                    recyclerView.setAdapter(adapter);
                }
            }
            // 데이터베이스 규칙에 엑세스 할 수 없을 때 호출되는 메서드
            public void onCancelled(@NonNull DatabaseError error) {
            }
        });

        // 리사이클러뷰 이벤트처리
        adapter.setOnItemClickListener(new SingleAdapter.OnItemClickListener() {
            @Override
            // 아이템 이벤트 처리
            // 아이템이 클릭되면 해당하는 안심 식당의 네이버플레이스로 전환됨
            public void onItemClick(SingleAdapter.ViewHolder holder, View view, int position) {
                SingleItem item = adapter.getItem(position);
                Toast.makeText(getContext(), item.getName() + " 검색을 시작합니다", Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://map.naver.com/v5/search/" + item.getName()));
                startActivity(intent);
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