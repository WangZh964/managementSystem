// 这个脚本用于为所有页面组件添加主题支持
// 它会自动为每个CSS文件添加主题变量支持

import * as fs from 'fs';

// 定义主题替换规则的接口
interface ThemeReplacement {
  pattern: RegExp;
  replacement: string;
}

// 需要处理的CSS文件列表
const cssFiles: string[] = [
  'd:\\managementProject\\frontend\\src\\views\\admin\\AdminList.css',
  'd:\\managementProject\\frontend\\src\\views\\user\\UserList.css',
  'd:\\managementProject\\frontend\\src\\views\\chart\\ChartList.css',
  'd:\\managementProject\\frontend\\src\\views\\city\\CityList.css',
  'd:\\managementProject\\frontend\\src\\views\\city\\CityAdd.css',
  'd:\\managementProject\\frontend\\src\\views\\order\\OrderList.css',
  'd:\\managementProject\\frontend\\src\\views\\pretty\\PrettyList.css',
  'd:\\managementProject\\frontend\\src\\views\\task\\TaskList.css',
  'd:\\managementProject\\frontend\\src\\views\\user\\UserProfile.css'
];

// 主题变量替换规则
const themeReplacements: ThemeReplacement[] = [
  {
    pattern: /background:\s*linear-gradient\([^)]*#[^)]*\)/g,
    replacement: 'background: var(--background-color, linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%))'
  },
  {
    pattern: /background:\s*rgba\(255,\s*255,\s*255,\s*[^)]*\)/g,
    replacement: 'background: var(--card-background, rgba(255, 255, 255, 0.85))'
  },
  {
    pattern: /background-color:\s*#[^;]*;/g,
    replacement: 'background-color: var(--card-background, rgba(255, 255, 255, 0.85));'
  }
];

/**
 * 处理单个CSS文件，添加主题支持
 * @param cssFile CSS文件路径
 */
function processCssFile(cssFile: string): void {
  try {
    if (fs.existsSync(cssFile)) {
      let content: string = fs.readFileSync(cssFile, 'utf8');
      
      // 检查是否已经导入了主题CSS
      if (!content.includes('@import url')) {
        content = '@import url(\'@/assets/css/theme.css\');\n\n' + content;
      }
      
      // 应用主题变量替换
      themeReplacements.forEach((replacement: ThemeReplacement) => {
        content = content.replace(replacement.pattern, replacement.replacement);
      });
      
      // 写入修改后的内容
      fs.writeFileSync(cssFile, content, 'utf8');
      console.log(`✅ 已更新: ${cssFile}`);
    } else {
      console.log(`❌ 文件不存在: ${cssFile}`);
    }
  } catch (error) {
    console.error(`❌ 处理文件 ${cssFile} 时出错:`, error);
  }
}

/**
 * 主函数，处理所有CSS文件
 */
function main(): void {
  console.log('🚀 开始为页面组件添加主题支持...\n');
  
  // 处理每个CSS文件
  cssFiles.forEach((cssFile: string) => {
    processCssFile(cssFile);
  });
  
  console.log('\n🎉 主题支持添加完成！');
}

// 执行主函数
main();