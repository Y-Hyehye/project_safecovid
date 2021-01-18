package com.example.project.ui.restaurant.local;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.project.R;

import java.util.ArrayList;


public class SingleAdapter extends RecyclerView.Adapter<SingleAdapter.ViewHolder> {
    Context context;

    //뷰가 아닌 데이터만을 보관
    ArrayList<SingleItem> items = new ArrayList<SingleItem>();

    //클릭이벤트처리 관련 사용자 정의
    OnItemClickListener listener;
    public  static interface  OnItemClickListener{
        public void onItemClick(ViewHolder holder, View view, int position);
    }

    public SingleAdapter(Context context){
        this.context =  context;
    }

    //어댑터에서 관리하고 있는 아이템을 관리하고 있는 개수만큼 반환
    @Override
    public int getItemCount() {
        return items.size();
    }

    //뷰홀더가 만들어지는 시점에 호출 됨
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View itemView = inflater.inflate(R.layout.singleitem, viewGroup, false);

        return new ViewHolder(itemView);
    }

    //각각의 아이템을 위한 뷰의 xml파일과 결합될 시 자동으로 불러와짐
    @Override
    public void onBindViewHolder(@NonNull ViewHolder viewHolder, int position) {
        // 리사이클러뷰에서 몇번째 아이템이 언제 노출이 되어야하는지 시점을 알려주기 위함
        SingleItem item = items.get(position);
        // 이를 홀더에넣어서 뷰홀더에 있는 뷰에 데이터 설정
        viewHolder.setItem(item);
        //클릭리스너
        viewHolder.setOnItemClickListener(listener);
    }

    // 아이템을 한개만 추가할 때
    public  void addItem(SingleItem item){
        items.add(item);
    }

    // 아이템을 여러개 추가할 때
    public void addItems(ArrayList<SingleItem> items){
        this.items = items;
    }

    public SingleItem getItem(int position){
        return  items.get(position);
    }

    //클릭리스너관련
    public void setOnItemClickListener(OnItemClickListener listener){
        this.listener = listener;
    }

    //뷰홀더(뷰홀더 객체는 뷰를 담아두는 역할을 하면서 동시에 뷰에 표시될 데이터를 설정하는 역할)
    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tv_name;
        TextView tv_address;
        TextView tv_number;
        TextView tv_type;

        //클릭이벤트처리관련 변수
        OnItemClickListener listenr;

        //각각의 아이템을 위한 뷰를 담음
        public ViewHolder(@NonNull final View itemView) {
            super(itemView);

            tv_name = (TextView) itemView.findViewById(R.id.name);
            tv_address = (TextView) itemView.findViewById(R.id.address);
            tv_number = (TextView) itemView.findViewById(R.id.number);
            tv_type = (TextView) itemView.findViewById(R.id.type);

            //아이템 클릭이벤트처리
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    int position = getAdapterPosition();
                    if(listenr != null ){
                        listenr.onItemClick(ViewHolder.this, itemView, position);
                    }
                }
            });
        }
        // SingleItem 객체를 전달받아 뷰홀더 안에 있는 뷰에 데이터를 설정
        public void setItem(SingleItem item) {
            tv_name.setText(item.getName());
            tv_address.setText(item.getAddress());
            tv_number.setText(item.getNumber());
            tv_type.setText(item.getType());
        }
        //클릭이벤트처리
        public void setOnItemClickListener(OnItemClickListener listenr){
            this.listenr = listenr;
        }

    }
}
