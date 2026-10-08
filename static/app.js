const form=document.querySelector('#plan-form'),statusEl=document.querySelector('#status'),submit=document.querySelector('#submit');
for(const field of form.querySelectorAll('textarea')){
 const counter=document.getElementById(field.getAttribute('aria-describedby'));
 const update=()=>{const length=Array.from(field.value).length;counter.textContent=`남은 글자수 ${Math.max(0,field.maxLength-length)}자 / 최대 ${field.maxLength}자 (공백 포함)`;};
 field.addEventListener('input',update);update();
}
if(/KAKAOTALK/i.test(navigator.userAgent))document.querySelector('#kakao').hidden=false;
document.querySelector('#copy-url').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);document.querySelector('#copy-result').textContent='주소를 복사했습니다.';}catch{prompt('아래 주소를 복사해주세요.',location.href);}});
form.addEventListener('submit',async event=>{
 event.preventDefault();statusEl.textContent='';
 if(!form.reportValidity())return;
 if(!form.querySelector('input[name=concepts]:checked')){statusEl.textContent='탐방 컨셉을 한 개 이상 선택해주세요.';return;}
 submit.disabled=true;submit.textContent='PDF를 만들고 있습니다…';
 try{
  const response=await fetch(form.action,{method:'POST',body:new FormData(form)});
  if(!response.ok){let message='PDF 생성에 실패했습니다. 입력 내용을 확인해주세요.';try{message=(await response.json()).error||message;}catch{}throw new Error(message);}
  const blob=await response.blob();const url=URL.createObjectURL(blob);const link=document.createElement('a');
  const number=Number(form.elements.group_no.value);const team=form.elements.team_name.value.trim().replace(/[\\/:*?"<>|\u0000-\u001f]/g,'_').replace(/^[ .]+|[ .]+$/g,'')||'조이름';
  link.href=url;link.download=`현장체험계획서_${number}조_${team}.pdf`;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);
  statusEl.textContent='PDF가 생성되었습니다. 다운로드 목록을 확인해주세요.';
 }catch(error){statusEl.textContent=error.message||'연결 오류가 발생했습니다. 다시 시도해주세요.';}
 finally{submit.disabled=false;submit.textContent='계획서 PDF 저장하기';}
});
