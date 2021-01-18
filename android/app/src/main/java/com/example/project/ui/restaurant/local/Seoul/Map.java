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
import com.example.project.R;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.naver.maps.geometry.LatLng;
import com.naver.maps.map.CameraPosition;
import com.naver.maps.map.MapView;
import com.naver.maps.map.NaverMap;
import com.naver.maps.map.OnMapReadyCallback;
import com.naver.maps.map.overlay.Marker;
import com.naver.maps.map.overlay.Overlay;


public class Map extends Fragment implements OnMapReadyCallback, Overlay.OnClickListener {

    // MapView 선언
    private MapView mapView;
    // NaverMap 선언
    private static NaverMap naverMap;

    // DatabaseReference 선언
    private DatabaseReference reference;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View root =  inflater.inflate(R.layout.map_seoul, container, false);

        // MapView 리소스 아이디 가져오기
        mapView = (MapView) root.findViewById(R.id.map_view);

        // MapView onCreate 호출
        mapView.onCreate(savedInstanceState);

        naverMapBasicSettings();

        return root;
    }

    // NaverMap 객체 얻어오기
    public void naverMapBasicSettings() {
        mapView.getMapAsync(this::onMapReady);
    }

    // NaverMap 인스턴스가 준비되면 호출되는 콜백 메서드
    // 맵뷰 시작 할 때 위치 지정
    public void onMapReady(@NonNull final NaverMap naverMap) {
        CameraPosition cameraPosition = new CameraPosition(
                new LatLng(37.5547044, 126.9669926),
                11); // 위도, 경도, 줌 레벨 지정
        naverMap.setCameraPosition(cameraPosition);

        // DatabaseReference 인스턴스 가져오기
        reference = FirebaseDatabase.getInstance().getReference();

        // restaurant(자식노드) 위치에 접근
        Query query = reference.child("restaurant");

        query.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // seoul의 데이터 개수 세기
                int cnt = (int)dataSnapshot.child("seoul").getChildrenCount();

                final String[] restaurant = new String[cnt];
                final double[] longitude = new double[cnt];
                final double[] latitude = new double[cnt];
                // 서울 내의 안심식당 식당명, 경도, 위도 값 가져오기
                for (int idx = 0; idx < cnt; idx++) {
                    restaurant[idx] = dataSnapshot.child("seoul").child(String.valueOf(idx)).child("사업장명").getValue(String.class);
                    longitude[idx] = dataSnapshot.child("seoul").child(String.valueOf(idx)).child("경도").getValue(Double.class);
                    latitude[idx] = dataSnapshot.child("seoul").child(String.valueOf(idx)).child("위도").getValue(Double.class);
                }

                for (int idx = 0; idx < cnt; idx++) {
                    // 마커 생성
                    final Marker marker = new Marker();
                    marker.setPosition(new LatLng(latitude[idx], longitude[idx]));
                    marker.setCaptionText(restaurant[idx]);
                    marker.setCaptionRequestedWidth(200);
                    marker.setMap(naverMap);

                    // 마커 클릭이벤트 처리
                    // 마커가 클릭되면 해당하는 안심 식당의 네이버플레이스로 전환됨
                    marker.setOnClickListener(overlay -> {
                        Toast.makeText(getContext(), marker.getCaptionText() + " 검색을 시작합니다", Toast.LENGTH_SHORT).show();
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://map.naver.com/v5/search/" + marker.getCaptionText()));
                        startActivity(intent);
                        return false;
                    });
                }
            }

            // 데이터베이스 규칙에 엑세스 할 수 없을 때 호출되는 메서드
            @Override
            public void onCancelled(DatabaseError databaseError) {
                Toast.makeText(getContext(), "오류 발생~", Toast.LENGTH_SHORT).show();      // 에러가 났을 시에 토스트메시지로 알려줌
            }
        });
    }

    // OnClick 이벤트를 위한 메서드
    public boolean onClick(@NonNull Overlay overlay) {
        return false;
    }

    // 마커 변경
    private void setMark(Marker marker, double lat, double lng, int resourceID) {
    }
}