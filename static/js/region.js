const REGIONS = [
    ('seoul', '서울'),
    ('busan', '부산'),
    ('daegu', '대구'),
    ('incheon', '인천'),
    ('gwangju', '광주'),
    ('daejeon', '대전'),
    ('ulsan', '울산'),
    ('sejong', '세종'),
    ('gyeonggi', '경기'),
    ('gangwon', '강원'),
    ('chungbuk', '충북'),
    ('chungnam', '충남'),
    ('jeonbuk', '전북'),
    ('jeonnam', '전남'),
    ('gyeongbuk', '경북'),
    ('gyeongnam', '경남'),
    ('jeju', '제주')
]

const SEOUL_DISTRICTS = ['종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구']
const BUSAN_DISTRICTS = ['중구','서구','동구','영도구','부산진구','동래구','남구','북구','강서구','해운대구','사하구','금정구','연제구','수영구','사상구','기장군']
const DAEGU_DISTRICTS = ['중구','동구','서구','남구','북구','수성구','달서구','달성군','군위군']
const INCHEON_DISTRICTS = ['중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군']
const GWANGJU_DISTRICTS = ['동구','서구','남구','북구','광산구']
const DAEJEON_DISTRICTS = ['중구','서구','유성구','대덕구']
const ULSAN_DISTRICTS = ['중구','남구','동구','북구','울주군']
const SEJONG_DISTRICTS = ['조치원읍','연기면','연동면','부강면','금남면','장군면','연서면','전의면','전동면','소정면','한솔동','새롬동','나성동','다정동','도담동','어진동','해밀동','아름동','종촌동','고운동','보람동','대평동','소담동','반곡동']
const GYEONGGI_DISTRICTS = ['수원시 장안구','수원시 권선구','수원시 팔달구','수원시 영통구','성남시 수정구','성남시 중원구','성남시 분당구','의정부시','안양시 만안구','안양시 동안구','부천시 원미구','부천시 소사구','부천시 오정구','광명시','동두천시','평택시','안산시 상록구','안산시 단원구','고양시 덕양구','고양시 일산동구','고양시 일산서구','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시 처인구','용인시 기흥구','용인시 수지구','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주시','연천군','가평군','양평군']
const GANGWON_DISTRICTS = ['춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군']
const CHUNGBUK_DISTRICTS = ['청주시 상당구','청주시 흥덕구','청주시 서원구','청주시 청원구','충주시','제천시','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군']
const CHUNGNAM_DISTRICTS = ['천안시 동남구','천안시 서북구','공주시','보령시','아산시','서산시','논산시','계룡시','당진시','금산군','부여군','서천군','청양군','홍성군','예산군','태안군']
const JEONBUK_DISTRICTS = ['전주시 완산구','전주시 덕진구','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군']
const JEONNAM_DISTRICTS = ['목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군']
const GYEONGBUK_DISTRICTS = ['포항시 남구','포항시 북구','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군']
const GYEONGNAM_DISTRICTS = ['창원시 의창구','창원시 성산구','창원시 마산합포구','창원시 마산회원구','창원시 진해구','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군']
const JEJU_DISTRICTS = ['제주시','서귀포시']

const DISTRICTS = {
    'seoul':SEOUL_DISTRICTS,
    'busan':BUSAN_DISTRICTS,
    'daegu':DAEGU_DISTRICTS,
    'incheon':INCHEON_DISTRICTS,
    'gwangju':GWANGJU_DISTRICTS,
    'daejeon':DAEJEON_DISTRICTS,
    'ulsan':ULSAN_DISTRICTS,
    'sejong':SEJONG_DISTRICTS,
    'gyeonggi':GYEONGGI_DISTRICTS,
    'gangwon':GANGWON_DISTRICTS,
    'chungbuk':CHUNGBUK_DISTRICTS,
    'chungnam':CHUNGNAM_DISTRICTS,
    'jeonbuk':JEONBUK_DISTRICTS,
    'jeonnam':JEONNAM_DISTRICTS,
    'gyeongbuk':GYEONGBUK_DISTRICTS,
    'gyeongnam':GYEONGNAM_DISTRICTS,
    'jeju':JEJU_DISTRICTS
}

$(document).ready(function region() {
    let main_category_array = new Array();
    let main_category_object = new Object();

    mainCategoryObject = new Object();
          mainCategoryObject.main_category_id = "1";
          mainCategoryObject.main_category_name = "락";
          mainCategoryArray.push(mainCategoryObject);

    mainCategoryObject = new Object();
          mainCategoryObject.main_category_id = "2";
          mainCategoryObject.main_category_name = "R&B";
          mainCategoryArray.push(mainCategoryObject);

    let subCategoryArray = new Array();
          let subCategoryObject = new Object();

    subCategoryObject = new Object();
          subCategoryObject.main_category_id = "1";
          subCategoryObject.sub_category_id = "1"
          subCategoryObject.sub_category_name = "모던락"	
          subCategoryArray.push(subCategoryObject);
          
          subCategoryObject = new Object();
          subCategoryObject.main_category_id = "1";
          subCategoryObject.sub_category_id = "2"
          subCategoryObject.sub_category_name = "비주얼락"	
          subCategoryArray.push(subCategoryObject);
          
          subCategoryObject = new Object();
          subCategoryObject.main_category_id = "1";
          subCategoryObject.sub_category_id = "3"
          subCategoryObject.sub_category_name = "고스락"	
          subCategoryArray.push(subCategoryObject);
          
          subCategoryObject = new Object();
          subCategoryObject.main_category_id = "2";
          subCategoryObject.sub_category_id = "1"
          subCategoryObject.sub_category_name = "네오소울"	
          subCategoryArray.push(subCategoryObject);
          
          subCategoryObject = new Object();
          subCategoryObject.main_category_id = "2";
          subCategoryObject.sub_category_id = "2"
          subCategoryObject.sub_category_name = "힙합소울"	
          subCategoryArray.push(subCategoryObject);
          
          subCategoryObject = new Object();
          subCategoryObject.main_category_id = "2";
          subCategoryObject.sub_category_id = "3"
          subCategoryObject.sub_category_name = "뉴잭스윙"	
          subCategoryArray.push(subCategoryObject);
          
          subCategoryObject = new Object();
          subCategoryObject.main_category_id = "2";
          subCategoryObject.sub_category_id = "4"
          subCategoryObject.sub_category_name = "어반"	
          subCategoryArray.push(subCategoryObject);

    let mainCategorySelectBox = $("select[name='mainCategory']");
          
          for(let i=0;i<mainCategoryArray.length;i++){
              mainCategorySelectBox.append("<option value='"+mainCategoryArray[i].main_category_id+"'>"+mainCategoryArray[i].main_category_name+"</option>");
          }

    $(document).on("change","select[name='mainCategory']",function(){
              
              var subCategorySelectBox = $("select[name='subCategory']");
              subCategorySelectBox.children().remove();
      $("option:selected", this).each(function(){
        let selectValue = $(this).val();
        subCategorySelectBox.append("<option value=''>전체</option>");
                  for(var i=0;i<subCategoryArray.length;i++){
                      if(selectValue == subCategoryArray[i].main_category_id){
                          
                          subCategorySelectBox.append("<option value='"+subCategoryArray[i].sub_category_id+"'>"+subCategoryArray[i].sub_category_name+"</option>");
                          
                      }
                  }
              });
          });			
      });
